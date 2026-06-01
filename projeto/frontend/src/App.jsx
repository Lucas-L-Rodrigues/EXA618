import { useState } from "react";
import Mapa from "./components/Mapa";
import ListaBares from "./components/ListaBares";

function App() {
  const [posicao, setPosicao] = useState(null);
  const [bares, setBares] = useState([]);
  const [raio, setRaio] = useState(1);

  const API_URL =
    "https://exa618-projeto-bares.onrender.com";

  async function buscarBares() {
    if (!posicao) {
      alert("Clique no mapa primeiro.");
      return;
    }

    const resposta = await fetch(
      `${API_URL}/bares/mais-proximos?lat=${posicao.lat}&lon=${posicao.lng}`
    );

    const dados = await resposta.json();

    setBares(dados);
  }

  async function buscarPorRaio() {
    if (!posicao) {
      alert("Clique no mapa primeiro.");
      return;
    }

    if (raio <= 0) {
      alert("Informe um raio válido.");
      return;
    }

    const resposta = await fetch(
      `${API_URL}/bares/proximos?lat=${posicao.lat}&lon=${posicao.lng}&raio_km=${raio}`
    );

    const dados = await resposta.json();

    setBares(dados);
  }

  async function curtir(id) {
    await fetch(
      `${API_URL}/bares/${id}/like`,
      {
        method: "POST",
      }
    );

    // Atualiza a lista após curtir
    if (bares.length === 10) {
      buscarBares();
    } else {
      buscarPorRaio();
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Bares Próximos</h1>

      <Mapa setPosicao={setPosicao} />

      {posicao && (
        <>
          <p>
            Latitude: {posicao.lat}
          </p>

          <p>
            Longitude: {posicao.lng}
          </p>

          <button onClick={buscarBares}>
            Buscar 10 bares mais próximos
          </button>

          <div style={{ marginTop: "15px" }}>
            <label>
              Raio (km):
            </label>

            <input
              type="number"
              min="0.1"
              step="0.1"
              value={raio}
              onChange={(e) =>
                setRaio(e.target.value)
              }
              style={{
                marginLeft: "10px",
                marginRight: "10px",
                width: "80px",
              }}
            />

            <button onClick={buscarPorRaio}>
              Buscar bares por raio
            </button>
          </div>
        </>
      )}

      <ListaBares
        bares={bares}
        curtir={curtir}
      />
    </div>
  );
}

export default App;