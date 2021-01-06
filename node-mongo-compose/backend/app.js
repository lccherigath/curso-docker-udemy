const express = require('express');
const restful = require('node-restful');
const server = express();
const mongoose = restful.mongoose;
const bodyParser = require('body-parser');
const cors = require('cors');

// Database
// -- Associa a API de Promise do node à API de Promise do mongoose (mongoose.Promise deprecated)
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://db/mydb');

// // Teste
// server.get('/', (req, res, next) => res.send('Backend'));

// Middlewares
server.use(bodyParser.urlencoded({extended: true}));
server.use(bodyParser.json());
server.use(cors());

// ODM (Mapeamento Objeto-Documento)
const Client = restful.model(
  'Client',
  { name: { type: String, required: true } }
);

// REST API
Client.methods(['get', 'post', 'put', 'delete']);
Client.updateOptions({ new: true, runValidators: true });

// Routes
Client.register(server, '/clients');

// Start server
server.listen(3000);
