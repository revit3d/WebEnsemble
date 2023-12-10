<template>
    <div>
        <p class="p-6 text-5xl font-bold tracking-wider m-3">Create new model</p>

        <form @submit.prevent="submitForm">
        <div v-show="activeStep > 0">
            <p class="font-semibold text-3xl tracking-wide mb-5">Step 1: Choose model architecture</p>
            <label>
                <label class="ml-12 text-2xl">
                    <input type="radio" @click="nextStep" v-model="modelParams.model_type" value="random_forest"  :disabled="activeStep > 1"/>
                    Random Forest
                </label>
                <label class="ml-20 text-2xl">
                    <input type="radio" @click="nextStep" v-model="modelParams.model_type" value="gradient_boosting"  :disabled="activeStep > 1"/>
                    Gradient Boosting
                </label>
            </label>
        </div>

        <div v-show="activeStep > 1">
            <p class="font-semibold text-3xl tracking-wide mt-10 mb-5">Step 2: Specify ensemble parameters</p>
            <label class="ml-12 text-2xl">
                Number of estimators in the ensemble
                <input type="number" class="input-base" v-model="modelParams.n_estimators" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Maximum tree depth
                <input type="number" v-bind:class="[{'input-disabled': noMaxDepth}, 'input-base']" v-model="modelParams.max_depth" :disabled="noMaxDepth === true" />
                <br />
                <label class="ml-12">
                    No maximum tree depth
                </label>
                <input type="checkbox" v-model="noMaxDepth" class="input-base w-6 h-6" />
            </label>
            <br />
            <label class="mt-8 ml-12 text-2xl">
                Feature subsample ratio
                <input type="number" step="any" class="input-base" v-model="modelParams.feature_subsample_size" />
            </label>
            <div v-if="modelParams.model_type === 'gradient_boosting'">
                <label class="ml-12 text-2xl">
                    Learning rate
                    <input type="number" step="any" class="input-base" v-model="modelParams.learning_rate" />
                </label>
            </div>
            <div v-show="activeStep === 2" class="font-semibold text-2xl mt-8">
                <button :class="[isEnsParamsValid ? 'button-ready' : 'button-waiting', 'button-container']" @click="nextStep" :disabled="!isEnsParamsValid">Next</button>
            </div>
        </div>

        <div v-show="activeStep > 2">
            <p class="font-semibold text-3xl tracking-wide mt-10 mb-5">Step 3: Specify simple estimator parameters</p>
            <label class="ml-12 text-2xl">
                Split condition
                <select class="input-base" v-model="modelParams.splitter">
                    <option value="">--default condition--</option>
                    <option value="best">best</option>
                    <option value="random">random</option>
                </select>
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Minimal number of samples at an internal node
                <input type="number" class="input-base" v-model="modelParams.min_samples_split" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Minimal number of samples at a leaf node
                <input type="number" class="input-base" v-model="modelParams.min_samples_leaf" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Minimal weight fraction at a leaf node
                <input type="number" step="any" class="input-base" v-model="modelParams.min_weight_fraction_leaf" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Number of considered features
                <input type="number" class="input-base" v-model="modelParams.max_features" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Random state
                <input type="number" class="input-base" v-model="modelParams.random_state" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Maximum leaf nodes
                <input type="number" class="input-base" v-model="modelParams.max_leaf_nodes" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Minimal impurity decrease
                <input type="number" step="any" class="input-base" v-model="modelParams.min_impurity_decrease" />
            </label>
            <br />
            <label class="ml-12 text-2xl">
                Cost-Complexity Pruning parameter
                <input type="number" step="any" class="input-base" v-model="modelParams.ccp_alpha" />
            </label>
            <div class="font-semibold text-2xl mt-4">
                <button class="button-container button-ready" @click="submitForm">Submit</button>
            </div>
        </div>
        </form>
    </div>
</template>

<script>
export default {
  data() {
    return {
      activeStep: 1,
      noMaxDepth: false,
      modelParams: {
        model_type: null,

        n_estimators: null,
        learning_rate: null,
        max_depth: null,
        feature_subsample_size: null,

        splitter: null,
        min_samples_split: null,
        min_samples_leaf: null,
        min_weight_fraction_leaf: null,
        max_features: null,
        random_state: null,
        max_leaf_nodes: null,
        min_impurity_decrease: null,
        ccp_alpha: null,
      },
    };
  },
  computed: {
    isEnsParamsValid() {
      return this.modelParams.n_estimators && (this.noMaxDepth || this.modelParams.max_depth);
    },
  },
  methods: {
    nextStep() {
      if (this.activeStep < 3) {
        this.activeStep++;
      }
    },
    submitForm() {
      // Handle form submission logic here
    },
  },
};
</script>

<style scoped>
@import '@/assets/ButtonStyle.css';
@import '@/assets/InputStyle.css';
</style>