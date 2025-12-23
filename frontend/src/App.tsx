import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { Manage } from './pages/Manage/Manage.tsx';
import { Login } from './pages/Login';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AIAdvisor } from './pages/AIAdvisor.tsx';
import { Reports } from './pages/Reports.tsx';
import { Dashboard } from './pages/Dashboard.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Login Page */}
        <Route path="/login" element={<Login />} />

        {/* All these routes require a login and use the Sidebar layout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout>
                <Dashboard />
              </MainLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/manage"
          element={
            <ProtectedRoute>
              <MainLayout>
                <Manage />
              </MainLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/ai"
          element={
            <ProtectedRoute>
              <MainLayout>
                <AIAdvisor />
              </MainLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <MainLayout>
                <Reports />
              </MainLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
