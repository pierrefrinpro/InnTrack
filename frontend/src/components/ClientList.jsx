import React, { useState, useEffect } from 'react';
import { clientsAPI } from '../services/api';
import ClientForm from './ClientForm';

function ClientList() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      const response = await clientsAPI.getAll();
      const clientsData = Array.isArray(response.data) 
        ? response.data 
        : response.data.results || [];
      
      setClients(clientsData);
      setLoading(false);
    } catch (err) {
      console.error('Erreur complète:', err);
      setError(`Erreur: ${err.message}`);
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Supprimer ce client ?')) {
      try {
        await clientsAPI.delete(id);
        loadClients();
      } catch (err) {
        alert('Erreur lors de la suppression');
      }
    }
  };

  if (loading) return <div>Chargement...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h1>InnTrack - Gestion des Clients</h1>
      
      <ClientForm onClientAdded={loadClients} />
      
      <h2>Liste des Clients ({clients.length})</h2>
      {clients.length === 0 ? (
        <p>Aucun client enregistré</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0' }}>
            <th style={{ border: '1px solid #ddd', padding: '8px' }}>Type</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Nom</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Email</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Téléphone</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {clients.map(client => (
              <tr key={client.id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{client.type}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{client.nom}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{client.email}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{client.telephone}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <button 
                    onClick={() => handleDelete(client.id)}
                    style={{ padding: '5px 10px', cursor: 'pointer', backgroundColor: '#ff4444', color: 'white', border: 'none' }}
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ClientList;
