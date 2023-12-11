<template>
    <div>
        <p class="p-6 text-5xl font-bold tracking-wider m-3">Model {{ $route.params.id }} info</p>
        <p class="text-3xl font-semibold tracking-wide m-3">Model status: </p>
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
        <div class="mt-12 flex gap-10 font-semibold text-2xl">
            <button class="button-container button-ready" @click="navigateTo('/model/fit/' + this.$route.params.id)">Fit model</button>
            <button :class="['button-container', isModelFitted ? 'button-ready' : 'button-waiting']" @click="navigateTo('/model/predict/' + this.$route.params.id)" :disabled="!isModelFitted">Make predictions</button>
        </div>
    </div>
</template>

<script>
export default defineNuxtComponent ({
    data() {
        return {
            modelParams: {
                model_type: 'gradient_boosting',
                is_trained: true,
                ensemble_params: {
                    n_estimators: 'None',
                    learning_rate: 'None',
                    max_depth: 'None',
                    feature_subsample_size: 'None',
                },
                tree_params: {
                    splitter: 'None',
                    min_samples_split: 'None',
                    min_samples_leaf: 'None',
                    min_weight_fraction_leaf: 'None',
                    max_features: 'None',
                    random_state: 'None',
                    max_leaf_nodes: 'None',
                    min_impurity_decrease: 'None',
                    ccp_alpha: 'None',
                },
            },
        };
    },
    computed: {
        isModelFitted() {
            return this.modelParams.is_trained;
        },
    },
    async asyncData({ _route }) {
        try {
            const response = await $fetch('http://localhost:8000/model/' + _route.params.id);
            console.log(response)
            return {
                modelParams: response,
            };
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    },
    mounted() {
        const websocket = new WebSocket('ws://localhost:8000/model/fit');

        websocket.onmessage = () => {}
    }
})
</script>

<style scoped>
@import '@/assets/ButtonStyle.css';
        .output-base {
        display:inline-block;
        position: relative;
        height: 100%;
        width: 60%;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 5px;
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