<script setup>
import { ref } from 'vue';

const props = defineProps(['realized', 'forecasted', 'ticker', 'forecastLength']);

const getDataRealized = () => {
  return {
  labels: props.realized.date,
  datasets: [
    {
      label: props.ticker + " Approx. Returns (%)",
      backgroundColor: '#f87979',
      data: props.realized.returns,
    }
  ]
  }
}

const getDataForecasted = () => {
  return {
  labels: props.forecasted.date,
  datasets: [
    {
      label: props.ticker + " Approx. Returns (%)",
      backgroundColor: '#e81481',
      data: props.forecasted.returns,
    }
  ]
}
}

const getOptionsRealized = () => {
  return {
    scales: {
      y: {
        suggestedMin: -15,
        suggestedMax: 15
      }
    }
  }
}

const getOptionsForecasted = () => {
  return {
    scales: {
      y: {
        suggestedMin: -0.5,
        suggestedMax: 0.5
      }
    }
  }
}

</script>

<script>
import {Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title,Tooltip,Legend} from 'chart.js'
import { ref } from 'vue';
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip,Legend)
</script>

<template>
    <h3>Realized Returns (approximated)</h3>
    <Line :data="getDataRealized()" :options="getOptionsRealized()"/>
    <h3>Forecasted Returns ({{ props.forecastLength }}-day forecast, approximated)</h3>
    <Line :data="getDataForecasted()" :options="getOptionsForecasted()"/>
</template>