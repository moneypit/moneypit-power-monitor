var express = require('express');
var child_process = require('child_process');
const bodyParser = require("body-parser");
var router = express.Router();

router.get('/', function(req, res, next) {
  res.json(swagger);
});

router.get('/config', function(req, res, next) {
  res.json(config);
});

router.get('/power', function(req, res, next) {
  rClient.get("power", function(err, reply) {
    if (err) {
      res.json(err);
    } else {

      if (reply == null) {
        res.json({});
      } else {
        res.json(JSON.parse(reply));
      }

    }

  });
});

module.exports = router;
