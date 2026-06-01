import { useState } from "react";
import Mapa from "./components/Mapa";
import ListaBares from "./components/ListaBares";

function App() {
  const [posicao, setPosicao] = useState(null);
  const [bares, setBares] = useState([]);

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

  async function curtir(id) {
    await fetch(
      `${API_URL}/bares/${id}/like`,
      {
        method: "POST",
      }
    );

    buscarBares();
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
            Buscar bares próximos
          </button>
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