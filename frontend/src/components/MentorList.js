import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../utils/api';

const MentorList = () => {
  const { user } = useAuth();
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [techStackFilter, setTechStackFilter] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [requestMessage, setRequestMessage] = useState('');
  const [requestLoading, setRequestLoading] = useState(false);

  useEffect(() => {
    fetchMentors();
  }, [techStackFilter, searchTerm, sortBy]);

  const fetchMentors = async () => {
    try {
      const params = new URLSearchParams();
      if (techStackFilter) params.append('tech_stack', techStackFilter);
      if (searchTerm) params.append('search', searchTerm);
      if (sortBy) params.append('sort_by', sortBy);

      const response = await api.get(`/mentors?${params.toString()}`);
      setMentors(response.data);
    } catch (err) {
      setError('Failed to load mentors');
    } finally {
      setLoading(false);
    }
  };

  const handleRequestMatching = async (mentorId) => {
    setRequestLoading(true);
    setError('');

    try {
      const response = await api.post('/matching-requests', {
        mentor_id: mentorId,
        message: requestMessage,
      });

      if (response.status === 200 || response.status === 201) {
        alert('매칭 요청이 성공적으로 전송되었습니다!');
        setSelectedMentor(null);
        setRequestMessage('');
      }
    } catch (err) {
      setError(err.response?.data?.detail || '매칭 요청에 실패했습니다.');
    } finally {
      setRequestLoading(false);
    }
  };

  if (user?.role !== 'mentee') {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          멘티만 멘토 목록을 볼 수 있습니다.
        </div>
      </div>
    );
  }

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
        <h1 className="text-3xl font-bold text-gray-900 mb-6">멘토 찾기</h1>
        
        {/* Search and Filter Controls */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                멘토 이름 검색
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="멘토 이름으로 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                기술 스택 필터
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="기술 스택으로 필터링..."
                value={techStackFilter}
                onChange={(e) => setTechStackFilter(e.target.value)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                정렬
              </label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="name">이름순</option>
                <option value="tech_stack">기술 스택순</option>
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Mentor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mentors.map((mentor) => (
            <div key={mentor.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <img
                    className="h-16 w-16 rounded-full object-cover mr-4"
                    src={mentor.profile_image_url}
                    alt={mentor.name}
                  />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {mentor.name}
                    </h3>
                    <p className="text-sm text-gray-500">멘토</p>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-gray-600 text-sm">
                    {mentor.bio || '소개글이 없습니다.'}
                  </p>
                </div>

                {mentor.tech_stack && mentor.tech_stack.length > 0 && (
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-1">
                      {mentor.tech_stack.map((tech, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <button
                  onClick={() => setSelectedMentor(mentor)}
                  className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md text-sm font-medium hover:bg-indigo-700"
                >
                  매칭 요청
                </button>
              </div>
            </div>
          ))}
        </div>

        {mentors.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">검색 조건에 맞는 멘토가 없습니다.</p>
          </div>
        )}
      </div>

      {/* Matching Request Modal */}
      {selectedMentor && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                매칭 요청
              </h3>
              <div className="mt-4">
                <p className="text-sm text-gray-500 mb-4">
                  {selectedMentor.name} 멘토에게 매칭 요청을 보내시겠습니까?
                </p>
                
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  rows={4}
                  placeholder="간단한 메시지를 남겨주세요 (선택사항)"
                  value={requestMessage}
                  onChange={(e) => setRequestMessage(e.target.value)}
                />
              </div>
              
              <div className="flex justify-center space-x-4 mt-6">
                <button
                  onClick={() => {
                    setSelectedMentor(null);
                    setRequestMessage('');
                  }}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  disabled={requestLoading}
                >
                  취소
                </button>
                <button
                  onClick={() => handleRequestMatching(selectedMentor.id)}
                  disabled={requestLoading}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {requestLoading ? '전송 중...' : '요청 보내기'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MentorList;
