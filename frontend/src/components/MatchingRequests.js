import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../utils/api';

const MatchingRequests = () => {
  const { user } = useAuth();
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState(null);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await api.get('/matching-requests');
      setRequests(response.data);
    } catch (err) {
      setError('Failed to load matching requests');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateRequest = async (requestId, status) => {
    setActionLoading(requestId);
    setError('');

    try {
      await api.put(`/matching-requests/${requestId}`, { status });
      await fetchRequests(); // Refresh the list
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update request');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteRequest = async (requestId) => {
    if (!window.confirm('정말로 이 요청을 삭제하시겠습니까?')) {
      return;
    }

    setActionLoading(requestId);
    setError('');

    try {
      await api.delete(`/matching-requests/${requestId}`);
      await fetchRequests(); // Refresh the list
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete request');
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'accepted':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'pending':
        return '대기중';
      case 'accepted':
        return '수락됨';
      case 'rejected':
        return '거절됨';
      default:
        return status;
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          {user?.role === 'mentor' ? '매칭 요청' : '내 요청'}
        </h1>

        {error && (
          <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {requests.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500">
              {user?.role === 'mentor' 
                ? '아직 받은 매칭 요청이 없습니다.' 
                : '아직 보낸 매칭 요청이 없습니다.'}
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {requests.map((request) => (
              <div key={request.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 mr-3">
                        {user?.role === 'mentor' 
                          ? `멘티 ID: ${request.mentee_id}` 
                          : `멘토 ID: ${request.mentor_id}`}
                      </h3>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(request.status)}`}>
                        {getStatusText(request.status)}
                      </span>
                    </div>
                    
                    {request.message && (
                      <div className="mb-4">
                        <h4 className="text-sm font-medium text-gray-700 mb-1">메시지:</h4>
                        <p className="text-gray-600 text-sm bg-gray-50 p-3 rounded">
                          {request.message}
                        </p>
                      </div>
                    )}
                    
                    <div className="text-sm text-gray-500">
                      <p>요청 일시: {new Date(request.created_at).toLocaleString('ko-KR')}</p>
                      {request.updated_at !== request.created_at && (
                        <p>업데이트: {new Date(request.updated_at).toLocaleString('ko-KR')}</p>
                      )}
                    </div>
                  </div>

                  <div className="ml-6 flex flex-col space-y-2">
                    {user?.role === 'mentor' && request.status === 'pending' && (
                      <>
                        <button
                          onClick={() => handleUpdateRequest(request.id, 'accepted')}
                          disabled={actionLoading === request.id}
                          className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 disabled:opacity-50"
                        >
                          {actionLoading === request.id ? '처리 중...' : '수락'}
                        </button>
                        <button
                          onClick={() => handleUpdateRequest(request.id, 'rejected')}
                          disabled={actionLoading === request.id}
                          className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 disabled:opacity-50"
                        >
                          {actionLoading === request.id ? '처리 중...' : '거절'}
                        </button>
                      </>
                    )}

                    {user?.role === 'mentee' && (
                      <button
                        onClick={() => handleDeleteRequest(request.id)}
                        disabled={actionLoading === request.id}
                        className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 disabled:opacity-50"
                      >
                        {actionLoading === request.id ? '삭제 중...' : '삭제'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchingRequests;
