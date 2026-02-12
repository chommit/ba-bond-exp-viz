import { useState } from "react"
import axios from "axios"
import { GIFTS } from "./gifts"
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis
} from "recharts"

const COLORS = [
  "#8884d8", "#82ca9d", "#ffc658",
  "#ff8042", "#8dd1e1"
]

export default function App() {
  const [selectedGifts, setSelectedGifts] = useState([])
  const [result, setResult] = useState(null)

  const addGift = (gift) => {
    if (selectedGifts.find(g => g.gift_id === gift.id)) return
    setSelectedGifts([...selectedGifts, {
      gift_id: gift.id,
      name: gift.name,
      value: (gift.grade === "yellow") ? 1 : 2
    }])
  }

  const updateValue = (gift_id, value) => {
    setSelectedGifts(selectedGifts.map(g =>
      g.gift_id === gift_id ? { ...g, value } : g
    ))
  }
  const removeGift = (gift_id) => {
    setSelectedGifts(selectedGifts.filter(g => g.gift_id !== gift_id))
  }

  const runCompute = async () => {
    const res = await axios.post("http://localhost:8000/compute", {
      gifts: selectedGifts.map(({ gift_id, value }) => ({ gift_id, value }))
    })
    setResult(res.data)
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>EXP per Month Simulator</h1>

      <h3>Add Preferred Gifts</h3>
      <select onChange={e => {
        const gift = GIFTS.find(g => g.id === Number(e.target.value))
        if (gift) addGift(gift)
      }}>
        <option value="">Select a gift</option>
        {GIFTS.map(g => (
          <option key={g.id} value={g.id}>{g.name}</option>
        ))}
      </select>

      {selectedGifts.map(g => (
        <div
          key={g.gift_id}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            marginBottom: "6px"
          }}
        >
          <span style={{ minWidth: "150px" }}>{g.name}</span>

          <select
            value={g.value}
            onChange={e => updateValue(g.gift_id, Number(e.target.value))}
          >
            <option value={1}>Nice</option>
            <option value={2}>Great</option>
            <option value={3}>Amazing</option>
          </select>

          <button
            onClick={() => removeGift(g.gift_id)}
            style={{
              backgroundColor: "#ff4d4d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              padding: "1px 4px"
            }}
          >
            ✕
          </button>
        </div>
      ))}

      <br />
      <button onClick={runCompute}>Run Simulation</button>

      {result && (
        <>
          <h2>Total EXP: {Math.trunc(result.total_exp[1])}</h2>

          <BarChart width={500} height={80} data={[
            { name: "EXP", value: result.total_exp[1] }
          ]}>
            <XAxis type="number" domain={[0, 24000]} />
            <Bar dataKey="value" />
          </BarChart>

          <PieChart width={400} height={400}>
            <Pie
              data={result.components.map((v, i) => ({
                name: `${v[0]}`,
                value: Math.trunc(v[1])
              }))}
              dataKey="value"
              cx="50%"
              cy="50%"
              outerRadius={140}
            >
              {result.components.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </>
      )}
    </div>
  )
}
