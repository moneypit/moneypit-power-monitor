new Vue({
  el: '#mp-fan-controller',
  data: {
    device: '',
    location: '',
    power_last_updated: '',

    amps: [],
    kwh: []

  },

  methods: {

  },

  created () {
    var vm = this;

    axios.get('./api/config')
    .then(function (response) {
      vm.device = response.data.device;
      vm.location = response.data.location;
    })

    axios.get('./api/power')
    .then(function (response) {

      vm.amps[0] = response.data.power_usage_0.amps.toFixed(3);
      vm.kwh[0] = response.data.power_usage_0.kwh.toFixed(3);

      vm.amps[1] = response.data.power_usage_1.amps.toFixed(3);
      vm.kwh[1] = response.data.power_usage_1.kwh.toFixed(3);

      vm.amps[2] = response.data.power_usage_2.amps.toFixed(3);
      vm.kwh[2] = response.data.power_usage_2.kwh.toFixed(3);

      vm.power_last_updated = response.data.timestamp;
    })

  }
})
