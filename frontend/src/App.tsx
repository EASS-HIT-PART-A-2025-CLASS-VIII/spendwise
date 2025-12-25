import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { Manage } from './pages/Manage/Manage.tsx';
import { Login } from './pages/Login';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AIAdvisor } from './pages/AIAdvisor.tsx';
import { Reports } from './pages/Reports.tsx';
import { Dashboard } from './pages/Dashboard.tsx';
import { Register } from './pages/Register.tsx';
import { AIProvider } from './context/AIContext.tsx';

function App() {
  return (
    <AIProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Login and register Page */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* protected routes*/}
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
    </AIProvider>
  );
}

export default App;
