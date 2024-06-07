<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    console.log("Scores page mounted");
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
  <div class="container">
    <h1>Tableau des scores</h1>
    <table>
      <thead>
        <tr>
          <th class="top">ID</th>
          <th>Player Name</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.id">
          <td>{{ scoreEntry.id }}</td>
          <td class="test">{{ scoreEntry.playerName }}</td>
          <td>{{ scoreEntry.score }}</td>
        </tr>
      </tbody>
  </table>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1 {
    font-size: 2em;
    margin-top: 5vh;
  }

  table {
    width: 40%;
    border-collapse: collapse;
    background-color: #ACECA1;
    border-radius: 10px;
  }

  th {
    background-color: #6C9D6B;
    color: white;
  }
  
  th, td {
    padding: 8px;
    text-align: center;
  }
</style>
