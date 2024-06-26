<template>
  <div>
    <p class="p-6 text-5xl font-bold tracking-wider m-3">Model <label class="text-emerald-700"> {{ modelParams.model_name }} </label> info</p>
    <div class="text-3xl tracking-wide m-3">
      <label class="font-semibold mr-4">Model status:</label>
      <span :class="['dot-container', {'dot-green': isModelFitted, 'dot-yellow': isModelFitting,'dot-red': !isModelFitting}, 'mr-2']"></span>
      <label v-if="isModelFitted">Fitted</label>
      <label v-if="isModelFitting && !isModelFitted">Fitting</label>
      <label v-if="!isModelFitting && !isModelFitted">Not fitted</label>
    </div>
    <p class="text-3xl font-semibold tracking-wide m-3">Model parameters</p>

    <div class="ml-12 text-2xl">
      <p class="m-4 font-semibold">Ensemble parameters</p>
      <div class="flex flex-col space-y-4">
        <div class="flex">
          <div class="w-3/5">
            Model architecture
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.model_type === null ? 'Undefined' : modelParams.model_type }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Number of estimators in the ensemble
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.ensemble_params.n_estimators === null ? 'Undefined' : modelParams.ensemble_params.n_estimators }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Maximum tree depth
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.ensemble_params.max_depth === null ? 'Undefined' : modelParams.ensemble_params.max_depth }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Feature subsample ratio
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.ensemble_params.feature_subsample_size === null ? 'Undefined' : modelParams.ensemble_params.feature_subsample_size }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Learning rate
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.ensemble_params.learning_rate === null ? 'Undefined' : modelParams.ensemble_params.learning_rate }}</output>
          </div>
        </div>
      </div>

      <p class="m-4 font-semibold">Simple estimator parameters</p>
      <div class="flex flex-col space-y-4">
        <div class="flex">
          <div class="w-3/5">
            Split condition
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.splitter === null ? 'Undefined' : modelParams.tree_params.splitter }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Minimal number of samples at an internal node
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.min_samples_split === null ? 'Undefined' : modelParams.tree_params.min_samples_split }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Minimal number of samples at a leaf node
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.min_samples_leaf === null ? 'Undefined' : modelParams.tree_params.min_samples_leaf }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Minimal weight fraction at a leaf node
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.min_weight_fraction_leaf === null ? 'Unidefined' : modelParams.tree_params.min_weight_fraction_leaf }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Number of considered features
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.max_features === null ? 'Undefined' : modelParams.tree_params.max_features }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Random state
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.random_state === null ? 'Undefined' : modelParams.tree_params.random_state }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Maximum leaf nodes
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.max_leaf_nodes === null ? 'Undefined' : modelParams.tree_params.max_leaf_nodes }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Minimal impurity decrease
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.min_impurity_decrease === null ? 'Undefined' : modelParams.tree_params.min_impurity_decrease }}</output>
          </div>
        </div>
        <div class="flex">
          <div class="w-3/5">
            Cost-Complexity Pruning parameter
          </div>
          <div class="w-2/5">
            <output class="output-base">{{ modelParams.tree_params.ccp_alpha === null ? 'Undefined' : modelParams.tree_params.ccp_alpha }}</output>
          </div>
        </div>
      </div>
    </div>
    <div v-show="isModelFitted">
      <p class="ml-16 mt-4 mb-4 text-2xl font-semibold">MSE on train and validation datasets</p>
      <LineChart :chartData="chartData" :chartOptions="chartOptions"/>
    </div>
    <div class="mt-12 flex gap-10 font-semibold text-2xl">
      <button class="button-container button-ready" @click="navigateTo('/model/fit/' + this.$route.params.id)">Fit model</button>
      <button :class="['button-container', isModelFitted ? 'button-ready' : 'button-waiting']" @click="navigateTo('/model/predict/' + this.$route.params.id)" :disabled="!isModelFitted">Make predictions</button>
      <button :class="['button-container', (isModelFitting || isModelFitted) ? 'button-ready' : 'button-waiting']" @click="fetchFile(modelParams.train_dataset_file_path)" :disabled="!(isModelFitted || isModelFitting)">Download<br />train file</button>
      <button :class="['button-container', ((isModelFitting || isModelFitted) && (modelParams.val_dataset_file_path !== null)) ? 'button-ready' : 'button-waiting']" @click="fetchFile(modelParams.val_dataset_file_path)" :disabled="!((isModelFitted || isModelFitting) && (modelParams.val_dataset_file_path !== null))">Download<br />validation file</button>
    </div>
  </div>
</template>

<script>
import { useStore } from '@/store';
import LineChart from '@/components/LineChart.vue';

export default defineNuxtComponent({
  components: {
    LineChart
  },
  computed: {
    isModelFitted() {
    console.log(this.modelParams.val_dataset_file_path);
      const store = useStore();
      let modelStatus = store.modelStates.find(obj => obj.id === this.$route.params.id);
      return modelStatus.is_trained;
    },
    isModelFitting() {
      const store = useStore();
      let modelStatus = store.modelStates.find(obj => obj.id === this.$route.params.id);
      return (modelStatus.target_name !== null) && !modelStatus.is_trained;
    },
    chartData() {
      const store = useStore();
      let modelStatus = store.modelStates.find(obj => obj.id === this.$route.params.id);
      if (modelStatus.is_trained) {
        return {
          labels: Array.from({ length: this.modelParams.train_loss.length }, (_, index) => index + 1),
          datasets: [
            {
              data: this.modelParams.train_loss,
              label: 'Train loss',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
            {
              data: this.modelParams.val_loss,
              label: 'Validation loss',
              backgroundColor: 'rgba(255, 0, 0, 0.2)',
              borderColor: 'rgba(255, 0, 0, 1)',
              borderWidth: 1,
            }
          ]
        };
      } else {
        return { labels: [], datasets: [] }
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            labels: {
              font: {
                size: 22,
              },
            },
          },
        },
      };
    },
  },
  async asyncData ({ payload }) {
    try {
      const store = useStore();
      const apiUrl = process.server ? store.API_URL_SERVER : store.API_URL_CLIENT
      const response = await $fetch('http://' + apiUrl + '/api' + payload.path);
      return { modelParams: response };
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  },
  methods: {
    async fetchFile(fileUrl) {
      const store = useStore();
      const apiUrl = process.server ? store.API_URL_SERVER : store.API_URL_CLIENT
      window.location.href = 'http://' + apiUrl + '/' + fileUrl;
    },
  },
});
</script>

<style scoped>
@import '@/assets/ButtonStyle.css';
@import '@/assets/DotStyle.css';
.output-base {
  display:inline-block;
  height: 100%;
  width: 60%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: whitesmoke;
}
.button-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  width: 208px;
  padding: 6px;
  border-radius: 3px;
  cursor: pointer;
}
</style>