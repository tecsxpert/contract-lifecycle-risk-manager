import { useEffect, useState, useContext } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Contracts() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);

  const { token } = useContext(AuthContext);

  useEffect(() => {
    fetchContracts();
  }, [page]);

  const fetchContracts = async () => {
    try {
      const res = await api.get(`/contracts?page=${page}&size=5`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setContracts(res.data.content || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    try {
      const res = await api.get(`/contracts/search?q=${query}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setContracts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/contracts/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      fetchContracts();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Contracts</h1>

      <Link to="/dashboard">
        <button className="bg-purple-500 text-white px-4 py-2 mr-2 mb-4">
          Go to Dashboard
        </button>
      </Link>

      <Link to="/create">
        <button className="bg-blue-500 text-white px-4 py-2 mb-4">
          Create Contract
        </button>
      </Link>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Search contracts..."
          className="border p-2 mr-2"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleSearch}
          className="bg-green-500 text-white px-4 py-2"
        >
          Search
        </button>
      </div>

      {contracts.length === 0 ? (
        <p>No contracts found</p>
      ) : (
        <>
          <table className="w-full border">
            <thead>
              <tr className="bg-gray-200">
                <th className="p-2 border">Title</th>
                <th className="p-2 border">Status</th>
                <th className="p-2 border">Risk</th>
                <th className="p-2 border">Actions</th>
              </tr>
            </thead>

            <tbody>
              {contracts.map((c) => (
                <tr key={c.id}>
                  {/* 🔹 CLICKABLE TITLE → DETAIL PAGE */}
                  <td className="p-2 border">
                    <Link
                      to={`/contracts/${c.id}`}
                      className="text-blue-600 underline"
                    >
                      {c.title}
                    </Link>
                  </td>

                  <td className="p-2 border">{c.status}</td>
                  <td className="p-2 border">{c.risk_level}</td>

                  <td className="p-2 border">
                    <button
                      className="bg-red-500 text-white px-2 py-1 mr-2"
                      onClick={() => handleDelete(c.id)}
                    >
                      Delete
                    </button>

                    <Link to={`/edit/${c.id}`}>
                      <button className="bg-yellow-500 text-white px-2 py-1">
                        Edit
                      </button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="mt-4">
            <button
              className="bg-gray-300 px-3 py-1 mr-2"
              disabled={page === 0}
              onClick={() => setPage(page - 1)}
            >
              Prev
            </button>

            <button
              className="bg-gray-300 px-3 py-1"
              onClick={() => setPage(page + 1)}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Contracts;