import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './components/pages/Dashboard';
import ToutesLesDonnees from './components/pages/ToutesLesDonnees';
import Devis from './components/pages/Devis';
import Realisations from './components/pages/Realisations';
import FactureFournisseurs from './components/pages/FactureFournisseurs';
import FactureClients from './components/pages/FactureClients';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="donnees" element={<ToutesLesDonnees />} />
          <Route path="devis" element={<Devis />} />
          <Route path="realisations" element={<Realisations />} />
          <Route path="factures-fournisseurs" element={<FactureFournisseurs />} />
          <Route path="factures-clients" element={<FactureClients />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
