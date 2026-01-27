import React, { useState } from 'react';
import { clientsAPI } from '../services/api';

function ClientForm({ onClientAdded }) {
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    email: '',
    telephone: '',
    adresse: '',
    type: 'PARTICULIER'
  });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(`Changement: ${name} = ${value}`); // Pour débugger
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log('Données envoyées:', formData);
    
    try {
      await clientsAPI.create(formData);
      
      // Reset du formulaire
      setFormData({ 
        nom: '', 
        prenom: '',
        email: '', 
        telephone: '', 
        adresse: '',
        type: 'PARTICULIER'
      });
      setError(null);
      
      if (onClientAdded) onClientAdded();
      
      alert('Client ajouté avec succès !');
    } catch (err) {
      console.error('Erreur complète:', err);
      console.error('Détails erreur:', err.response?.data);
      setError(`Erreur: ${JSON.stringify(err.response?.data)}`);
    }
  };

  return (
    <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
      <h2>➕ Ajouter un client</h2>
      {error && <div style={{ color: 'red', marginBottom: '10px', padding: '10px', backgroundColor: '#ffebee', borderRadius: '4px' }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        {/* Type de client */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Type de client *
          </label>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          >
            <option value="PARTICULIER">👤 Particulier</option>
            <option value="PROFESSIONNEL">🏢 Entreprise</option>
          </select>
          <small style={{ color: '#666' }}>Valeur actuelle: {formData.type}</small>
        </div>

        {/* Nom */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Nom {formData.type === 'PROFESSIONNEL' ? '(Raison sociale)' : ''} *
          </label>
          <input
            type="text"
            name="nom"
            placeholder={formData.type === 'PROFESSIONNEL' ? 'Nom de l\'entreprise' : 'Nom du client'}
            value={formData.nom}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          />
        </div>

        {/* Prénom (seulement pour particuliers) */}
        {formData.type === 'PARTICULIER' && (
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Prénom
            </label>
            <input
              type="text"
              name="prenom"
              placeholder="Prénom"
              value={formData.prenom}
              onChange={handleChange}
              style={{ 
                width: '100%', 
                padding: '10px', 
                borderRadius: '4px', 
                border: '1px solid #ddd',
                fontSize: '14px'
              }}
            />
          </div>
        )}

        {/* Email */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Email *
          </label>
          <input
            type="email"
            name="email"
            placeholder="exemple@email.com"
            value={formData.email}
            onChange={handleChange}
            required
            style={{ 
              width: '100%', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          />
        </div>

        {/* Téléphone */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Téléphone
          </label>
          <input
            type="tel"
            name="telephone"
            placeholder="06 12 34 56 78"
            value={formData.telephone}
            onChange={handleChange}
            style={{ 
              width: '100%', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #ddd',
              fontSize: '14px'
            }}
          />
        </div>

        {/* Adresse */}
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
            Adresse
          </label>
          <textarea
            name="adresse"
            placeholder="Adresse complète"
            value={formData.adresse}
            onChange={handleChange}
            rows="3"
            style={{ 
              width: '100%', 
              padding: '10px', 
              borderRadius: '4px', 
              border: '1px solid #ddd',
              fontSize: '14px',
              fontFamily: 'inherit'
            }}
          />
        </div>

        <button 
          type="submit"
          style={{ 
            padding: '12px 24px', 
            backgroundColor: '#4CAF50', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold'
          }}
        >
          ✅ Ajouter le client
        </button>
      </form>
    </div>
  );
}

export default ClientForm;
