<template>
    <div v-if="!isPredsAvailable">
        <form @submit.prevent="uploadFile">
            <p class="p-6 text-5xl font-bold tracking-wider m-3">Make predictions</p>
            <p class="font-semibold text-3xl tracking-wide mb-5">Upload dataset file</p>
            <input type="file" @change="handleTestFileUpload" class="mb-6" />
            <button type="submit" :class="[isFileUploaded ? 'button-ready' : 'button-waiting', 'button-container', 'font-semibold', 'text-2xl', 'mt-4']" :disabled="!isFileUploaded">Submit</button>
        </form>
    </div>

    <div v-if="isPredsAvailable">
        <p>{{ this.predictions }}</p>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                testFile: undefined,
                predictions: undefined,
            };
        },
        computed: {
            isFileUploaded() {
                return this.testFile;
            },
            isPredsAvailable() {
                return this.predictions;
            },
        },
        methods: {
            handleTestFileUpload(event) {
                this.testFile = event.target.files[0];
            },
            async uploadFile() {
                const formData = new FormData();
                formData.append('test_file', this.testFile);

                try {
                    const response = await $fetch('http://localhost:8000/model/predict/' + this.$route.params.id, {
                        method: 'POST',
                        body: formData,
                    });
                    console.log('Response:', response.data);
                    this.predictions = response.data;
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
</style>