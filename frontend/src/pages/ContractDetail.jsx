import { useEffect, useState, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";

function ContractDetail() {
  const { id } = useParams();
  const [contract, setContract] = useState(null);
  const { token } = useContext(AuthContext);

  useEffect(() => {
    api.get(`/contracts/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => setContract(res.data))
      .catch((err) => console.error(err));
  }, [id]);

  if (!contract) return <p>Loading...</p>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">{contract.title}</h1>

      <p>Status: {contract.status}</p>

      {/* SCORE BADGE */}
      <span className="bg-purple-500 text-white px-2 py-1">
        Risk: {contract.risk_level}
      </span>

      <div className="mt-4">
        <Link to={`/edit/${contract.id}`}>
          <button className="bg-yellow-500 text-white px-3 py-1 mr-2">
            Edit
          </button>
        </Link>

        <button className="bg-red-500 text-white px-3 py-1">
          Delete
        </button>
      </div>
    </div>
  );
}

export default ContractDetail;