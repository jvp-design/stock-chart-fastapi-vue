<template>
  <apexchart
    type="bar"
    width="100%"
    height="20%"
    :series="series"
    :options="chartOptions"
  ></apexchart>
</template>

<script>
import { computed, defineComponent } from 'vue';
export default defineComponent({
  props: {
    volume: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const series = computed(() => props.volume);

    const chartOptions = computed(() => ({
      type: 'bar',
      brush: {
        enabled: true,
        target: 'candles',
      },
      dataLabels: {
        enabled: false,
      },
      plotOptions: {
        bar: {
          columnWidth: '80%',
        },
      },
      stroke: {
        width: 0,
      },
      xaxis: {
        type: 'datetime',
        axisBorder: {
          offsetX: 13,
        },
        categories: props.volume[0]?.data.map((e) => e.x.getTime()) ?? [],
      },
    }));

    return { series, chartOptions };
  },
});
</script>

<style scoped></style>
