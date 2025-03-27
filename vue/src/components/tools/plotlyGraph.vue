<template>
  <div :ref="`plotlyChart_${chartId}`" :key="`plotlyChart_${chartId}`"></div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  props: {
    chartData: {
      type: Object,
      default: null,
    },
    chartId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      plotlyChart: null,
    };
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      if (this.$refs[`plotlyChart_${this.chartId}`] && this.chartData) {
        try {
          Plotly.newPlot(
            this.$refs[`plotlyChart_${this.chartId}`],
            this.chartData.data,
            this.chartData.layout,
            { responsive: true }
          );
        } catch (error) {
          console.error("Error in Plotly.newPlot:", error);
        }
      }
    },
  },
};
</script>
