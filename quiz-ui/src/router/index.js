import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import ScoresView from '@/views/ScoresView.vue';
import QuestionsManger from '@/views/QuestionsManager.vue';
import AdminPage from '@/views/AdminPage.vue';
import QuestionEdition from '@/views/QuestionEdition.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'new-quiz',
      component: NewQuizPage,
    },
    {
      path: '/scores',
      name: 'scores',
      component: ScoresView,
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsManger,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPage,
    },
    {
      path: '/questions/edit/:id',
      name: 'edit-question',
      component: QuestionEdition,
      props: true,
    }
  ]
});

export default router;
