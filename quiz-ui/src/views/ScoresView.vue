<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    console.log("Scores page mounted");
    try {
        const response = await quizApiService.getQuizInfo();
        console.log("Scores récupérés : ", response); // Log the scores
        registeredScores.value = response; // Assign the scores array
    } catch (error) {
        console.error("Erreur lors de la récupération des scores : ", error);
    }
});
</script>

<template>
  <div class="container">
    <h1>Tableau des scores</h1>
    <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Username</th>
        <th>Date</th>
        <th>Score</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        <td>{{ scoreEntry.id }}</td>
        <td>{{ scoreEntry.username }}</td>
        <td>{{ scoreEntry.date }}</td>
        <td>{{ scoreEntry.score }}</td>
      </tr>
    </tbody>
  </table>
  </div>
</template>

<style scoped>
  .container{
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1{
    font-size: 2em;
    margin-top: 5vh;
  }
</style>