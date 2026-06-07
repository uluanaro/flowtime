import { useState } from 'react'
import TasksPage from './pages/TasksPage'
import './App.css'
import PlannerPage from './pages/PlannerPage'

function App() {
  const [page, setPage] = useState('tasks')

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="logo">⟡ FlowTime</div>
        <nav>
          <button
            className={page === 'tasks' ? 'nav-item active' : 'nav-item'}
            onClick={() => setPage('tasks')}
          >
            Задачи
          </button>
          <button
            className={page === 'planner' ? 'nav-item active' : 'nav-item'}
            onClick={() => setPage('planner')}
          >
            AI Планировщик
          </button>
        </nav>
      </aside>

      <main className="content">
        {page === 'tasks' && <TasksPage />}
        {page === 'planner' && <PlannerPage/>}
      </main>
    </div>
  )
}

export default App