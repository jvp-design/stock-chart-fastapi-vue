<template>
  <div
    class="mx-auto h-1/2 sm:h-4/6 lg:h-5/6"
    :class="series.length ? '' : 'flex items-center justify-center'"
  >
    <div v-if="series.length" class="h-full">
      <JVPCandlestick :series="series" :interval="interval" :symbol="symbol" />
      <JVPVolume :volume="volume" />
    </div>
    <div v-else id="chart" class="text-4xl flex items-center justify-center">
      Choose a company, interval, and dates below
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue';
import JVPCandlestick from './charts/JVPCandlestick.vue';
import JVPVolume from './charts/JVPVolume.vue';
export default defineComponent({
  components: { JVPVolume, JVPCandlestick },
  props: {
    symbol: {
      type: String,
      required: true,
    },
    interval: {
      type: String,
      required: true,
    },
    series: {
      type: Array,
      required: true,
    },
    volume: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const symbol = computed(() => props.symbol.toUpperCase());
    const interval = computed(() => props.interval);
    const series = computed(() => props.series);
    const volume = computed(() => props.volume);

    return {
      symbol,
      interval,
      series,
      volume,
    };
  },
});
</script>
