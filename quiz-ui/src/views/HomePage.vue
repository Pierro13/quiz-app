<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    console.log("Home page mounted");
    try {
        const response = await quizApiService.getQuizInfo();
        console.log("Scores récupérés : ", response.scores); // Log the scores
        registeredScores.value = response.scores; // Assign the scores array
    } catch (error) {
        console.error("Erreur lors de la récupération des scores : ", error);
    }
});
</script>

<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    <p>{{ scoreEntry.date }} - {{ scoreEntry.score }}</p>
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>
