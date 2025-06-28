import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import Signup from './components/Signup';
import Profile from './components/Profile';
import MentorList from './components/MentorList';
import MatchingRequests from './components/MatchingRequests';
import Navbar from './components/Navbar';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? children : <Navigate to="/profile" />;
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Navigate to="/profile" />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/login" 
              element={
                <PublicRoute>
                  <Login />
                </PublicRoute>
              } 
            />
            <Route 
              path="/signup" 
              element={
                <PublicRoute>
                  <Signup />
                </PublicRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <Navbar />
                  <Profile />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/mentors" 
              element={
                <ProtectedRoute>
                  <Navbar />
                  <MentorList />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/matching-requests" 
              element={
                <ProtectedRoute>
                  <Navbar />
                  <MatchingRequests />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
