import React, { useState, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user, updateProfile, uploadProfileImage } = useAuth();
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    bio: user?.bio || '',
    tech_stack: user?.tech_stack || [],
  });
  const [newTechStack, setNewTechStack] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const fileInputRef = useRef();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleAddTechStack = () => {
    if (newTechStack && !formData.tech_stack.includes(newTechStack)) {
      setFormData({
        ...formData,
        tech_stack: [...formData.tech_stack, newTechStack],
      });
      setNewTechStack('');
    }
  };

  const handleRemoveTechStack = (tech) => {
    setFormData({
      ...formData,
      tech_stack: formData.tech_stack.filter(t => t !== tech),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const result = await updateProfile(formData);
      if (result.success) {
        setSuccess('프로필이 성공적으로 업데이트되었습니다.');
        setEditing(false);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      setError('Only .jpg and .png files are allowed');
      return;
    }

    // Validate file size (1MB)
    if (file.size > 1024 * 1024) {
      setError('File size must be less than 1MB');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const result = await uploadProfileImage(file);
      if (result.success) {
        setSuccess('프로필 이미지가 성공적으로 업로드되었습니다.');
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Image upload failed');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-8">
          <div className="flex items-center mb-8">
            <div className="flex-shrink-0 mr-6">
              <img
                className="h-24 w-24 rounded-full object-cover"
                src={user.profile_image_url}
                alt={user.name}
              />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{user.name}</h1>
              <p className="text-sm text-gray-500">
                {user.role === 'mentor' ? '멘토' : '멘티'} • {user.email}
              </p>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="mt-2 text-sm text-indigo-600 hover:text-indigo-500"
                disabled={loading}
              >
                프로필 이미지 변경
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png"
                onChange={handleImageUpload}
                className="hidden"
              />
            </div>
            <div>
              {!editing ? (
                <button
                  onClick={() => {
                    setEditing(true);
                    setFormData({
                      name: user.name || '',
                      bio: user.bio || '',
                      tech_stack: user.tech_stack || [],
                    });
                  }}
                  className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
                >
                  프로필 수정
                </button>
              ) : (
                <div className="space-x-2">
                  <button
                    onClick={() => setEditing(false)}
                    className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-400"
                  >
                    취소
                  </button>
                </div>
              )}
            </div>
          </div>

          {error && (
            <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
              {success}
            </div>
          )}

          {editing ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  이름
                </label>
                <input
                  type="text"
                  name="name"
                  id="name"
                  required
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>

              <div>
                <label htmlFor="bio" className="block text-sm font-medium text-gray-700">
                  소개글
                </label>
                <textarea
                  name="bio"
                  id="bio"
                  rows={4}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={formData.bio}
                  onChange={handleChange}
                  placeholder="자신을 소개해주세요..."
                />
              </div>

              {user.role === 'mentor' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    기술 스택
                  </label>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {formData.tech_stack.map((tech, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800"
                      >
                        {tech}
                        <button
                          type="button"
                          onClick={() => handleRemoveTechStack(tech)}
                          className="ml-2 text-indigo-600 hover:text-indigo-800"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                      placeholder="기술 스택 추가 (예: React, Python)"
                      value={newTechStack}
                      onChange={(e) => setNewTechStack(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleAddTechStack();
                        }
                      }}
                    />
                    <button
                      type="button"
                      onClick={handleAddTechStack}
                      className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                    >
                      추가
                    </button>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setEditing(false)}
                  className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  취소
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
                >
                  {loading ? '저장 중...' : '저장'}
                </button>
              </div>
            </form>
          ) : (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">소개글</h3>
                <p className="text-gray-600">
                  {user.bio || '아직 소개글이 없습니다.'}
                </p>
              </div>

              {user.role === 'mentor' && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">기술 스택</h3>
                  <div className="flex flex-wrap gap-2">
                    {user.tech_stack && user.tech_stack.length > 0 ? (
                      user.tech_stack.map((tech, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800"
                        >
                          {tech}
                        </span>
                      ))
                    ) : (
                      <p className="text-gray-500">아직 기술 스택이 등록되지 않았습니다.</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
