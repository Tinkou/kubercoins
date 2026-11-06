import express from 'express';
import morgan from 'morgan';
import { createClient } from 'redis';

let shuttingDown = false;

const client = await createClient({
  url: "redis://redis",
  socket: {
    family: 0
  }
})
  .on("error", function (err) {
    console.error("Redis error", err);
  })
  .connect();

const app = express();

app.use(morgan('common'));

app.get('/', function (req, res) {
  res.redirect('/index.html');
});

app.get('/json', async (req, res) => {
  if (shuttingDown) {
    // Reject new requests while shutting down
    return res.status(503).json({ error: 'Server is shutting down' });
  }

  const coins = await client.hLen('wallet');
  const hashes = await client.get('hashes');
  const now = Date.now() / 1000;
  res.json({
    coins: coins,
    hashes: hashes,
    now: now
  });
});

app.use(express.static('files'));

const server = app.listen(80, function () {
  console.log('WEBUI running on port 80');
});

// Graceful shutdown on SIGTERM / SIGINT
async function shutdown(signal) {
  if (shuttingDown) return;
  shuttingDown = true;
  console.log(`Received ${signal}, starting graceful shutdown...`);

  // Stop accepting new connections
  server.close(async (err) => {
    if (err) {
      console.error('Error while closing HTTP server', err);
    }

    try {
      // Close Redis connection
      await client.quit();
    } catch (e) {
      console.error('Error while closing Redis client', e);
    } finally {
      // Exit the process once everything is closed
      process.exit(0);
    }
  });

  // Failsafe: force exit if shutdown takes too long
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 5000);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

