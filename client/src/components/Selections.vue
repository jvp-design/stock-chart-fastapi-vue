<template>
  <div>
    <JVPDialog :dialog="dialog" @closeDialog="closeDialog" />
    <form class="ml-5" @submit.prevent="handleSubmit">
      <div class="my-1">
        <JVPInput
          v-model="state.symbol"
          label="Symbol"
          id="symbol"
          name="symbol"
          type="text"
          placeholder="eg. MSFT"
          :vuelidate="v$.symbol"
          hint="Required, less than 6 characters"
          :autofocus="true"
        />
      </div>
      <div class="my-1">
        <JVPInput
          v-model="state.startDate"
          label="Start Date"
          id="start-date"
          name="startDate"
          type="date"
          :vuelidate="v$.startDate"
          hint="Optional"
        />
      </div>
      <div class="my-1">
        <JVPInput
          v-model="state.endDate"
          label="End Date"
          id="end-date"
          name="endDate"
          type="date"
          :vuelidate="v$.endDate"
          hint="Optional"
        />
      </div>
      <div class="my-1">
        <JVPSelect
          v-model="state.interval"
          label="Interval"
          id="interval"
          :options="intervals"
        />
      </div>
      <button
        type="submit"
        class="w-full h-12 px-6 mt-6 lg:mt-0 rounded-lg bg-indigo-700 text-indigo-100 transition-colors duration-150 hover:bg-indigo-800 focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="disabled"
      >
        <span
          v-if="loading"
          class="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-10 w-10 mx-auto block"
        ></span>
        <span v-else>Get Chart</span>
      </button>
    </form>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, computed } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, maxLength, helpers } from '@vuelidate/validators';
import JVPInput from './JVPInput.vue';
import JVPSelect from './JVPSelect.vue';
import JVPDialog from './JVPDialog.vue';

export default defineComponent({
  components: { JVPDialog, JVPInput, JVPSelect },
  emits: ['setData'],
  setup(_, { emit }) {
    const intervals = ['Daily', 'Weekly', 'Monthly'];

    const state = reactive({
      symbol: '',
      interval: 'Daily',
      startDate: '',
      endDate: '',
    });

    const dialog = ref(false);

    const closeDialog = () => (dialog.value = false);

    const mustBeEarlierDate = helpers.withMessage(
      'Start date must be earlier than end date.',
      (value) => {
        const endDate = computed(() => state.endDate);
        if (!value || !endDate.value) return true;
        if (!checkDateFormat(endDate.value)) return true;
        return new Date(value) < new Date(endDate.value);
      }
    );

    const checkDateFormat = (param) => {
      if (!param) return true;
      return new Date(param).toString() !== 'Invalid Date';
    };

    const validateDateFormat = helpers.withMessage(
      'Please enter a valid date.',
      checkDateFormat
    );

    const rules = {
      symbol: { required, maxLength: maxLength(5) },
      startDate: {
        validateDateFormat,
        mustBeEarlierDate,
      },
      endDate: {
        validateDateFormat,
      },
    };
    const v$ = useVuelidate(rules, state);

    const disabled = computed(() => {
      return v$.value.$invalid;
    });

    const loading = ref(false);

    const preProcessData = () => {
      // Create the querystring
      const query = {};
      if (!!state.startDate) query.start = state.startDate;
      if (!!state.endDate) query.end = state.endDate;

      const queryString = Object.keys(query)
        .filter((key) => !!query[key])
        .map((key) => {
          return `${encodeURIComponent(key)}=${encodeURIComponent(query[key])}`;
        })
        .join('&');

      // Convert human-readable interval into yfinance style
      const interval =
        state.interval === 'Daily'
          ? '1d'
          : state.interval === 'Weekly'
          ? '1wk'
          : '1mo';

      // Create URL string and add query if it exists
      let url = `http://localhost:8000/quote/${state.symbol}/${interval}`;
      if (queryString.length) url = `${url}?${queryString}`;
      return url;
    };

    const fetchData = async (url) => {
      const response = await fetch(url);
      return await response.json();
    };

    const postProcessData = (res) => {
      // Parse dates
      const formatDate = (d) => new Date(d).toISOString().substr(0, 10);
      const dates = res.map((e) => e.date).sort();
      if (!state.startDate) {
        state.startDate = formatDate(dates[0]);
      }
      if (!state.endDate) {
        state.endDate = formatDate(dates[dates.length - 1]);
      }

      // Format the data
      const data = res.map((e) => ({
        x: new Date(e.date),
        y: e.data,
      }));
      const volData = res.map((e) => ({
        x: new Date(e.date),
        y: e.volume ?? 0,
      }));
      return {
        series: [{ data }],
        symbol: state.symbol,
        interval: state.interval,
        volume: [{ name: 'volume', data: volData }],
      };
    };

    const handleSubmit = async () => {
      v$.value.$validate();
      if (!v$.value.$invalid) {
        loading.value = true;
        try {
          const url = preProcessData();
          const res = await fetchData(url);
          const payload = postProcessData(res);

          emit('setData', payload);
        } catch (err) {
          console.log('err', err);
          dialog.value = true;
        }
        loading.value = false;
      }
    };

    return {
      intervals,
      state,
      disabled,
      loading,
      dialog,
      v$,
      handleSubmit,
      closeDialog,
    };
  },
});
</script>

<style scoped>
.loader {
  border-top-color: #6366f1;
  -webkit-animation: spinner 1.5s linear infinite;
  animation: spinner 1.5s linear infinite;
}

@-webkit-keyframes spinner {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spinner {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
