import { useState, useEffect } from 'react'
import { getTasks, createTask, deleteTask, estimateTask } from '../api'

function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [newTitle, setNewTitle] = useState('')
  const [estimate, setEstimate] = useState(null)

useEffect(() => {
  getTasks().then(response => {
    setTasks(response.data)
    })
}, [])

const handleCreate = () => {
  createTask({title: newTitle}).then(response => {
    setTasks([...tasks, response.data])
    setNewTitle('')
      })
}

const handleDelete = (id) => {
  deleteTask(id).then(() => {
    setTasks(tasks.filter(t => t.id !== id))
      })
    }

const handleEstimate = (task) => {
  estimateTask({ title: task.title, description: task.description })
    .then(response => setEstimate(response.data))
}

  return (
    <div>
      <h1>Задачи</h1>
      <input
      value={newTitle}
      onChange={e => setNewTitle(e.target.value)}
      placeholder="Новая задача..."
    />
    <button onClick={handleCreate}>Добавить</button>

     {tasks.map(task => (
      <div key={task.id} className="task-item">
        <span>{task.title}</span>
        <button onClick={() => handleDelete(task.id)}>Удалить</button>
        <button onClick={() => handleEstimate(task)}>AI оценка</button>

        {estimate && (
  <div className="estimate-box">
    <h3>⏱ {estimate.estimated_minutes} минут</h3>
    <p>{estimate.reasoning}</p>
    <ul>
      {estimate.tips.map((tip, i) => (
        <li key={i}>{tip}</li>
      ))}
    </ul>
  </div>
)}

      </div>
    ))}
    </div>
  )
}

export default TasksPage