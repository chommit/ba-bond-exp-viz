import { useState } from "react"
import axios from "axios"
import { GIFTS } from "./gifts"
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis
} from "recharts"

const COLORS = [
  "#827de5ff", "#82ca9d", "#ffc658",
  "#ff8042", "#8dd1e1", 
  "#e78dc0ff", "#f3eda8ff", "#f77d7dff",
  "#ab79c6ff", "#c7c7c7ff"

]

export default function App() {
  const [params, setParams] = useState({
    dailyHeadpats: 4,          // float 0–10
    craftingMonthlies: false,
    giftMonthlies: false,
    eligmaMiniKeystones: true,
    redBouquetPacks: 0,        // 0–24 int
    frrTryhard: false,
  });
  const [selectedGifts, setSelectedGifts] = useState([])
  const [result, setResult] = useState(null)

  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;

    setParams(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : Number(value)
    }));
  };

  const addGift = (gift) => {
    if (selectedGifts.find(g => g.gift_id === gift.id)) return
    setSelectedGifts([...selectedGifts, {
      gift_id: gift.id,
      name: gift.name,
      value: (gift.grade === "yellow") ? 1 : 2,
      grade: gift.grade
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
      gifts: selectedGifts.map(({ gift_id, value }) => ({ gift_id, value })),
      params: params
    })
    setResult(res.data)
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>BA EXP per Month Simulator</h1>

    <h2>Adjustables</h2>

    <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "400px" }}>

      <label>
        Daily Headpats: 
        <input
          type="number"
          name="dailyHeadpats"
          min="0"
          max="10"
          step="1"
          value={params.dailyHeadpats}
          onChange={handleChange}
        />
      </label>

      <label>
        Crafting Monthlies: 
        <input
          type="checkbox"
          name="craftingMonthlies"
          checked={params.craftingMonthlies}
          onChange={handleChange}
        />
      </label>

      <label>
        Gift Monthlies: 
        <input
          type="checkbox"
          name="giftMonthlies"
          checked={params.giftMonthlies}
          onChange={handleChange}
        />
      </label>

      <label>
        Eligma Shop Mini Keystones: 
        <input
          type="checkbox"
          name="eligmaMiniKeystones"
          checked={params.eligmaMiniKeystones}
          onChange={handleChange}
        />
      </label>

      <label>
        Red Bouquet Packs per Year: 
        <input
          type="number"
          name="redBouquetPacks"
          min="0"
          max="18"
          step="1"
          value={params.redBouquetPacks}
          onChange={handleChange}
        />
      </label>

      <label>
        FRR Tryhard: 
        <input
          type="checkbox"
          name="frrTryhard"
          checked={params.frrTryhard}
          onChange={handleChange}
        />
      </label>

    </div>

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
            {g.grade === "yellow" && (
              <option value={1}>Nice</option>
            )}
            <option value={2}>Great</option>
            <option value={3}>Amazing</option>
          </select>

          <button
            onClick={() => removeGift(g.gift_id)}
            style={{
              backgroundColor: "#ff4d4d",
              color: "#DDDDDDDD",
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

          <BarChart
            width={500}
            height={80}
            data={[{ name: "EXP", value: result.total_exp[1] }]}
            layout="vertical"
          >
            <XAxis type="number" domain={[0, 24000]} />
            <YAxis type="category" dataKey="name" hide />
            <Bar dataKey="value" fill="#FFB5D3" />
          </BarChart>

          <h3>EXP Per Crafting Keystone: {Math.round(result.exp_per_craft[1] * 100) / 100}</h3>

          <div style={{ display: "flex", alignItems: "center", gap: "40px" }}>
                {/* Pie Chart */}
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

                {/* Legend */}
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {result.components.map((comp, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <div
                        style={{
                          width: "20px",
                          height: "20px",
                          backgroundColor: COLORS[i % COLORS.length],
                          borderRadius: "4px"
                        }}
                      />
                      <span>{comp[0]}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
    </div>
  )
}
