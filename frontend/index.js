let temperaturChart;
let co2Chart;

export function chartDemo() {
  const ctx = document.getElementById("temperatur").getContext("2d");
  temperaturChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Temperatur"],
      datasets: [
        {
          label: "Temperatur",
          data: [],
          borderWidth: 1,
        },
      ],
    },
  });

  const co2Ctx = document.getElementById("co2").getContext("2d");
  co2Chart = new Chart(co2Ctx, {
    type: "line",
    data: {
      labels: ["CO2"],
      datasets: [
        {
          label: "CO2",
          data: [],
          borderWidth: 1,
        },
      ],
    },
  });
}

function connectToWebsiteMqtt() {
  const client = window.mqtt.connect("ws://localhost:9001");

  client.on("connect", function () {
    console.log("Connected to MQTT broker");
    client.subscribe("temperature", function (err) {
      if (!err) {
        console.log("Subscribed to temperature topic");
      } else {
        console.error("Subscription error:", err);
      }
    });
    client.subscribe("co2", function (err) {
      if (!err) {
        console.log("Subscribed to co2 topic");
      } else {
        console.error("Subscription error:", err);
      }
    });
  });

  client.on("message", function (topic, message) {
    console.log("Received message:", message.toString());
    console.log(topic);
    if (topic === "temperature") {
      updateTemperatureChart({
        label: new Date().toLocaleTimeString(),
        value: parseFloat(message.toString()),
      });
    } else if (topic === "co2") {
      updateCo2Chart({
        label: new Date().toLocaleTimeString(),
        value: parseFloat(message.toString()),
      });
    }
  });

  client.on("error", function (err) {
    console.error("Connection error:", err);
  });
}

function updateTemperatureChart(newData) {
  temperaturChart.data.labels.push(newData.label);
  temperaturChart.data.datasets[0].data.push(newData.value);
  temperaturChart.update();
}

function updateCo2Chart(newData) {
  co2Chart.data.labels.push(newData.label);
  co2Chart.data.datasets[0].data.push(newData.value);
  co2Chart.update();
}

document.addEventListener("DOMContentLoaded", (event) => {
  connectToWebsiteMqtt();
  chartDemo();
});
