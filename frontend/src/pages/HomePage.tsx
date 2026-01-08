import React, { useState } from 'react';
import { MagnifyingGlassIcon, MapPinIcon, CalendarIcon, UserGroupIcon } from '@heroicons/react/24/outline';

export const HomePage: React.FC = () => {
  const [searchData, setSearchData] = useState({
    destination: '',
    checkIn: '',
    checkOut: '',
    travelers: 1,
  });
  const [isCreateTripModalOpen, setIsCreateTripModalOpen] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Search data:', searchData);
    // TODO: Implement search functionality
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSearchData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section with Search */}
      <section className="relative bg-gradient-to-br from-primary-50 to-white dark:from-gray-900 dark:to-gray-800">
        <div className="container-booking">
          <div className="py-16 lg:py-24">
            <div className="text-center mb-12">
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                Создайте свои собственные путешествия
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                Планируйте маршруты, приглашайте друзей и делитесь впечатлениями от ваших поездок
              </p>
            </div>

            {/* Search Form */}
            <div className="max-w-4xl mx-auto">
              <form onSubmit={handleSearch} className="bg-white dark:bg-gray-800 rounded-booking-lg shadow-booking-lg p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  {/* Destination */}
                  <div className="relative">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Куда едем?
                    </label>
                    <div className="relative">
                      <MapPinIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="text"
                        name="destination"
                        value={searchData.destination}
                        onChange={handleInputChange}
                        placeholder="Город или регион"
                        className="booking-input pl-10"
                      />
                    </div>
                  </div>

                  {/* Check-in */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Когда?
                    </label>
                    <div className="relative">
                      <CalendarIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="date"
                        name="checkIn"
                        value={searchData.checkIn}
                        onChange={handleInputChange}
                        className="booking-input pl-10"
                      />
                    </div>
                  </div>

                  {/* Check-out */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      До какой даты?
                    </label>
                    <div className="relative">
                      <CalendarIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="date"
                        name="checkOut"
                        value={searchData.checkOut}
                        onChange={handleInputChange}
                        className="booking-input pl-10"
                      />
                    </div>
                  </div>

                  {/* Travelers */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Сколько человек?
                    </label>
                    <div className="relative">
                      <UserGroupIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <select
                        name="travelers"
                        value={searchData.travelers}
                        onChange={handleInputChange}
                        className="booking-input pl-10"
                      >
                        <option value={1}>1 человек</option>
                        <option value={2}>2 человека</option>
                        <option value={3}>3 человека</option>
                        <option value={4}>4 человека</option>
                        <option value={5}>5+ человек</option>
                      </select>
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full btn-primary flex items-center justify-center space-x-2"
                >
                  <MagnifyingGlassIcon className="w-5 h-5" />
                  <span>Начать планирование</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white dark:bg-gray-800">
        <div className="container-booking">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MapPinIcon className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Создавайте маршруты
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Планируйте поездки по любым направлениям и маршрутам
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <UserGroupIcon className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Совместное планирование
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Приглашайте друзей и планируйте поездки вместе
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CalendarIcon className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Делитесь впечатлениями
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Сохраняйте воспоминания и делитесь опытом с друзьями
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
