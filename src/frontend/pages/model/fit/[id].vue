<template>
    <div>
        <form @submit.prevent="uploadFiles">
            <p class="p-6 text-5xl font-bold tracking-wider m-3">Fit the model</p>
            <p class="font-semibold text-3xl tracking-wide mb-5">Upload train dataset file</p>
            <input type="file" @change="handleTrainFileUpload" class="mb-6" />
            <label class="ml-12 text-2xl">
                Target column:
                <input type="text" class="input-base" v-model="target_name" />
            </label>
            <p class="font-semibold text-3xl tracking-wide mb-5">Upload validation dataset file (optional)</p>
            <input type="file" @change="handleValFileUpload" class="mb-6" />
            <button type="submit" :class="[isTrainUploaded ? 'button-ready' : 'button-waiting', 'button-container', 'font-semibold', 'text-2xl', 'mt-4']" :disabled="!isTrainUploaded">Submit</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            target_name: undefined,
            trainFile: undefined,
            valFile: undefined,
        };
    },
    computed: {
        isTrainUploaded() {
            return this.target_name && this.trainFile;
        },
    },
    methods: {
        handleTrainFileUpload(event) {
            this.trainFile = event.target.files[0];
        },
        handleValFileUpload(event) {
            this.valFile = event.target.files[0];
        },
        async uploadFiles() {
            const formData = new FormData();
            formData.append('train_file', this.trainFile);
            if (this.valFile !== undefined) {
                formData.append('val_file', this.valFile);
            }
            formData.append('target_name', this.target_name);

            try {
                const response = await $fetch('http://localhost:8000/model/fit/' + this.$route.params.id, {
                    method: 'PUT',
                    body: formData,
                });
                // create a websocket to start fitting
                const websocket = new WebSocket('ws://localhost:8000/model/fit');
                websocket.onopen = () => {
                    websocket.send(this.$route.params.id);
                }
                await navigateTo('/model/' + this.$route.params.id);
            } catch (error) {
                console.error('Error:', error);
                throw error;
            }
        },
    },
};
</script>

<style scoped>
@import '@/assets/ButtonStyle.css';
@import '@/assets/InputStyle.css';
</style>