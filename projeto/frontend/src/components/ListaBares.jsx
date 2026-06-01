export default function ListaBares({ bares, curtir }) {
  return (
    <div>
      {bares.map((bar) => (
        <div
          key={bar.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            margin: "10px 0",
          }}
        >
          <h3>{bar.nome}</h3>

          <p>{bar.endereco}</p>

          <p>
            Distância: {bar.distancia_km.toFixed(2)} km
          </p>

          <p>
            Likes: {bar.likes}
          </p>

          <button onClick={() => curtir(bar.id)}>
            Curtir
          </button>
        </div>
      ))}
    </div>
  );
}