<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    console.log("Scores page mounted");
    try {
        const response = await quizApiService.getQuizInfo();
        console.log("Scores récupérés : ", response.scores);
        registeredScores.value = response.scores;
    } catch (error) {
        console.error("Erreur lors de la récupération des scores : ", error);
    }
});
</script>

<template>
  <div class="container">
    <h1>Tableau des scores</h1>
    <a href="/new-quiz" class="replay-link">
      Rejouer
    </a>
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

  .replay-link{
    border-radius: 5px;
    background-color: #ACECA1;
    margin: 0vh 0vw 3vh 0vw;
    padding: 1vh 1vh;
    text-decoration: none;
    color: inherit;
  }

  .replay-link:hover{
        background-color: #01a201;
    }
</style>
