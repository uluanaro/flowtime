import { useState } from 'react'
import { planDay} from '../api'

function PlannerPage() {
  const [date, setDate] = useState('')        // выбранная дата
  const [plan, setPlan] = useState(null)      // результат от AI
  const [loading, setLoading] = useState(false) // идёт ли запрос

  const handlePlan = () => {
  setLoading(true)          // показать спиннер
  planDay(date).then(response => {
    setPlan(response.data)  // сохранить результат
    setLoading(false)       // скрыть спиннер
  })
}

  return (
    <div>
      <h1>План на день:</h1>
      <input  type="date"
      value={date}
      onChange={e => setDate(e.target.value)}
      />
    <button onClick={handlePlan}>
        {loading ? "AI думает..." : "Составить план"}
    </button>


        {plan && (
  <div>
    {plan.schedule.map((item, index) => (
      <div key={index}>
        <span>{item.start} - {item.end}</span>
        <span>{item.task_title}</span>
      </div>
    ))}
  </div>
)}
    </div>
  )
}
export default PlannerPage