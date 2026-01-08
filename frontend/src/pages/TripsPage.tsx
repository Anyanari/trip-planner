import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, CalendarIcon, UserGroupIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { Trip } from '../types';
import { getTrips, createTrip, updateTrip, deleteTrip } from '../services/api';

export const TripsPage: React.FC = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTrip, setEditingTrip] = useState<Trip | null>(null);
  const [newTrip, setNewTrip] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: ''
  });

  useEffect(() => {
    loadTrips();
  }, []);

  const loadTrips = async () => {
    try {
      const data = await getTrips();
      setTrips(data);
    } catch (error) {
      console.error('Error loading trips:', error);
    }
  };

  const handleCreateTrip = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const tripWithUser = { ...newTrip, user_id: 1 }; // TODO: Get current user ID
      await createTrip(tripWithUser);
      setNewTrip({ title: '', description: '', start_date: '', end_date: '' });
      setShowCreateForm(false);
      loadTrips();
    } catch (error) {
      console.error('Error creating trip:', error);
    }
  };

  const handleEditTrip = (trip: Trip) => {
    setEditingTrip(trip);
    setNewTrip({
      title: trip.title,
      description: trip.description || '',
      start_date: trip.start_date || '',
      end_date: trip.end_date || ''
    });
  };

  const handleUpdateTrip = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTrip) return;
    
    try {
      await updateTrip(editingTrip.id, newTrip);
      setEditingTrip(null);
      setNewTrip({ title: '', description: '', start_date: '', end_date: '' });
      loadTrips();
    } catch (error) {
      console.error('Error updating trip:', error);
    }
  };

  const handleDeleteTrip = async (tripId: number) => {
    if (!confirm('Вы уверены, что хотите удалить эту поездку?')) return;
    
    try {
      await deleteTrip(tripId);
      loadTrips();
    } catch (error) {
      console.error('Error deleting trip:', error);
    }
  };

  return (
    <div className="container-booking py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Мои путешествия
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Управляйте вашими поездками и планируйте новые приключения
          </p>
        </div>
        <button 
          className="btn-primary flex items-center space-x-2"
          onClick={() => setShowCreateForm(true)}
        >
          <PlusIcon className="w-5 h-5" />
          <span>Создать поездку</span>
        </button>
      </div>

      {/* Create Form Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-booking-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Новая поездка
            </h2>
            <form onSubmit={handleCreateTrip}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Название
                </label>
                <input
                  type="text"
                  value={newTrip.title}
                  onChange={(e) => setNewTrip({...newTrip, title: e.target.value})}
                  className="booking-input"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Описание
                </label>
                <textarea
                  value={newTrip.description}
                  onChange={(e) => setNewTrip({...newTrip, description: e.target.value})}
                  className="booking-input"
                  rows={3}
                />
              </div>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Дата начала
                  </label>
                  <input
                    type="date"
                    value={newTrip.start_date}
                    onChange={(e) => setNewTrip({...newTrip, start_date: e.target.value})}
                    className="booking-input"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Дата окончания
                  </label>
                  <input
                    type="date"
                    value={newTrip.end_date}
                    onChange={(e) => setNewTrip({...newTrip, end_date: e.target.value})}
                    className="booking-input"
                    required
                  />
                </div>
              </div>
              <div className="flex space-x-3">
                <button type="submit" className="btn-primary flex-1">
                  Создать
                </button>
                <button 
                  type="button" 
                  className="btn-secondary flex-1"
                  onClick={() => setShowCreateForm(false)}
                >
                  Отмена
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Form Modal */}
      {editingTrip && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-booking-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Изменить поездку
            </h2>
            <form onSubmit={handleUpdateTrip}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Название
                </label>
                <input
                  type="text"
                  value={newTrip.title}
                  onChange={(e) => setNewTrip({...newTrip, title: e.target.value})}
                  className="booking-input"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Описание
                </label>
                <textarea
                  value={newTrip.description}
                  onChange={(e) => setNewTrip({...newTrip, description: e.target.value})}
                  className="booking-input"
                  rows={3}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Дата начала
                </label>
                <input
                  type="date"
                  value={newTrip.start_date}
                  onChange={(e) => setNewTrip({...newTrip, start_date: e.target.value})}
                  className="booking-input"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Дата окончания
                </label>
                <input
                  type="date"
                  value={newTrip.end_date}
                  onChange={(e) => setNewTrip({...newTrip, end_date: e.target.value})}
                  className="booking-input"
                  required
                />
              </div>
              <div className="flex space-x-3">
                <button type="submit" className="btn-primary flex-1">
                  Сохранить
                </button>
                <button 
                  type="button" 
                  className="btn-secondary flex-1"
                  onClick={() => {
                    setEditingTrip(null);
                    setNewTrip({ title: '', description: '', start_date: '', end_date: '' });
                  }}
                >
                  Отмена
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Trips List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {trips.length === 0 ? (
          <div className="col-span-full">
            <div className="booking-card p-8 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CalendarIcon className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                У вас пока нет поездок
              </h3>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Создайте свою первую поездку и начните планировать приключение
              </p>
              <button 
                className="btn-primary"
                onClick={() => setShowCreateForm(true)}
              >
                Создать поездку
              </button>
            </div>
          </div>
        ) : (
          trips.map(trip => (
            <div key={trip.id} className="booking-card">
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {trip.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  {trip.description}
                </p>
                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <CalendarIcon className="w-4 h-4 mr-1" />
                  {trip.start_date} - {trip.end_date}
                </div>
                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <UserGroupIcon className="w-4 h-4 mr-1" />
                  {trip.members?.length || 0} участников
                </div>
                <div className="flex space-x-2 mb-4">
                  <button 
                    onClick={() => handleEditTrip(trip)}
                    className="flex-1 flex items-center justify-center px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
                  >
                    <PencilIcon className="w-4 h-4 mr-1" />
                    Изменить
                  </button>
                  <button 
                    onClick={() => handleDeleteTrip(trip.id)}
                    className="flex-1 flex items-center justify-center px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition-colors"
                  >
                    <TrashIcon className="w-4 h-4 mr-1" />
                    Удалить
                  </button>
                </div>
                <Link 
                  to={`/trips/${trip.id}`} 
                  className="btn-primary w-full text-center"
                >
                  Открыть поездку
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
