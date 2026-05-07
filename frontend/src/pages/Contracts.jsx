import { useEffect, useState, useContext } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import FileUpload from "../components/FileUpload";

function Contracts() {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(true);

  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");

  const [status, setStatus] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [page, setPage] = useState(0);

  const { token } = useContext(AuthContext);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
      setPage(0);
    }, 500);

    return () => clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    fetchContracts();
  }, [page, debouncedQuery, status, startDate, endDate]);

  const fetchContracts = async () => {
    try {
      const res = await api.get(
        `/contracts/search?q=${debouncedQuery}&status=${status}&startDate=${startDate}&endDate=${endDate}&page=${page}&size=5`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setContracts(res.data.content || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
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

  const handleExport = async () => {
    try {
      const res = await api.get("/contracts/export", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "contracts.csv");
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="p-4 max-w-7xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Contracts</h1>
      <div className="mb-4 flex flex-col md:flex-row gap-2">
        <Link to="/dashboard">
          <button className="bg-purple-500 text-white px-4 py-2 w-full md:w-auto">
            Dashboard
          </button>
        </Link>

        <Link to="/create">
          <button className="bg-blue-500 text-white px-4 py-2 w-full md:w-auto">
            Create Contract
          </button>
        </Link>

        <button
          onClick={handleExport}
          className="bg-green-600 text-white px-4 py-2 w-full md:w-auto"
        >
          Export CSV
        </button>
      </div>
      <div className="mb-4">
        <FileUpload />
      </div>
      <div className="mb-4 flex flex-col md:flex-row gap-2 flex-wrap">
        <input
          type="text"
          placeholder="Search..."
          className="border p-2 w-full md:w-auto"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <select
          className="border p-2 w-full md:w-auto"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(0);
          }}
        >
          <option value="">All Status</option>
          <option value="ACTIVE">Active</option>
          <option value="PENDING">Pending</option>
          <option value="COMPLETED">Completed</option>
        </select>

        <input
          type="date"
          className="border p-2 w-full md:w-auto"
          value={startDate}
          onChange={(e) => {
            setStartDate(e.target.value);
            setPage(0);
          }}
        />

        <input
          type="date"
          className="border p-2 w-full md:w-auto"
          value={endDate}
          onChange={(e) => {
            setEndDate(e.target.value);
            setPage(0);
          }}
        />
      </div>
      {contracts.length === 0 ? (
        <p className="text-gray-500">No contracts found</p>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full border text-sm md:text-base">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2 border">Title</th>
                  <th className="p-2 border">Status</th>
                  <th className="p-2 border hidden md:table-cell">Risk</th>
                  <th className="p-2 border">Actions</th>
                </tr>
              </thead>

              <tbody>
                {contracts.map((c) => (
                  <tr key={c.id}>
                    <td className="p-2 border">
                      <Link
                        to={`/contracts/${c.id}`}
                        className="text-blue-600 underline"
                      >
                        {c.title}
                      </Link>
                    </td>

                    <td className="p-2 border">{c.status}</td>

                    <td className="p-2 border hidden md:table-cell">
                      {c.risk_level}
                    </td>

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
          </div>
          <div className="mt-4 flex justify-center md:justify-start">
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