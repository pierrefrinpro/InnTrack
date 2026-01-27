import React from 'react';
import { NavLink } from 'react-router-dom';

const BottomNavigation = () => {
  const navItems = [
    { path: '/', icon: '📊', label: 'Tableau de bord' },
    { path: '/donnees', icon: '📁', label: 'Toutes les données' },
    { path: '/devis', icon: '📄', label: 'Devis' },
    { path: '/realisations', icon: '🏗️', label: 'Réalisations' },
    { path: '/factures-fournisseurs', icon: '📥', label: 'Factures Fourn.' },
    { path: '/factures-clients', icon: '📤', label: 'Factures Clients' },
  ];

  return (
    <nav className="bottom-nav">
      <ul className="nav-items">
        {navItems.map((item) => (
          <li key={item.path} className="nav-item">
            <NavLink
              to={item.path}
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
              end={item.path === '/'}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default BottomNavigation;
