import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Trip, Suggestion, Route, Expense, OSMPlace, User } from '../types';
import { RouteBuilder } from '../components/RouteBuilder';
import {
  getTrip,
  getSuggestions,
  getTripRoutes,
  getTripExpenses,
  getUsers,
  addTripMember,
  searchPlaces,
  createPlace,
  createSuggestion,
  voteOnSuggestion,
  updateSuggestionStatus,
  createExpense,
  getTripBalances,
} from '../services/api';
import {
  UserGroupIcon,
  MapPinIcon,
  CalendarIcon,
  CurrencyDollarIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  CheckCircleIcon,
  XCircleIcon,
  HandThumbUpIcon,
  HandThumbDownIcon,
  ChatBubbleLeftRightIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

export const TripDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [trip, setTrip] = useState<Trip | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [activeTab, setActiveTab] = useState<'info' | 'suggestions' | 'routes' | 'expenses'>('info');
  const [suggestionFilter, setSuggestionFilter] = useState<'voting' | 'accepted' | 'rejected'>('voting');

  const currentUserId = 1;

  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [inviteUsername, setInviteUsername] = useState<string>('');

  const [suggestionQuery, setSuggestionQuery] = useState<string>('');
  const [suggestionSearchResults, setSuggestionSearchResults] = useState<OSMPlace[]>([]);
  const [isSearchingSuggestions, setIsSearchingSuggestions] = useState<boolean>(false);


  const [newExpense, setNewExpense] = useState({
    title: '',
    amount: '',
    paid_by: String(currentUserId),
    currency: 'RUB',
  });

  const [balances, setBalances] = useState<any[]>([]);

  useEffect(() => {
    if (id) {
      loadTripData(parseInt(id));
    }
  }, [id]);

  const loadTripData = async (tripId: number) => {
    try {
      const [tripData, suggestionsData, routesData, expensesData] = await Promise.all([
        getTrip(tripId),
        getSuggestions(tripId),
        getTripRoutes(tripId),
        getTripExpenses(tripId)
      ]);
      
      setTrip(tripData);
      setSuggestions(suggestionsData);
      setRoutes(routesData);
      setExpenses(expensesData);
    } catch (error) {
      console.error('Error loading trip data:', error);
    }
  };

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const users = await getUsers();
        setAllUsers(users);
      } catch (error) {
        console.error('Error loading users:', error);
      }
    };
    loadUsers();
  }, []);

  useEffect(() => {
    const loadBalances = async () => {
      if (!trip || activeTab !== 'expenses') return;
      try {
        const data = await getTripBalances(trip.id);
        setBalances(data);
      } catch (error) {
        console.error('Error loading balances:', error);
        setBalances([]);
      }
    };
    loadBalances();
  }, [activeTab, trip]);

  const isMember = (userId: number) => {
    return Boolean(trip?.members?.some((m) => m.id === userId));
  };

  const handleInviteUser = async (username: string) => {
    if (!trip) return;
    
    console.log('Searching for username:', username);
    console.log('Available users:', allUsers.map(u => ({ id: u.id, username: u.username, email: u.email })));
    
    const user = allUsers.find(u => u.username === username);
    console.log('Found user:', user);
    
    if (!user) {
      console.error('User not found:', username);
      // Попробуем поиск по частичному совпадению (без учета регистра)
      const foundUser = allUsers.find(u => 
        u.username.toLowerCase() === username.toLowerCase().trim()
      );
      console.log('Found user with case-insensitive search:', foundUser);
      
      if (foundUser) {
        // Если нашли без учета регистра, используем этого пользователя
        try {
          await addTripMember(trip.id, { user_id: foundUser.id, role: 'member' });
          await loadTripData(trip.id);
          setInviteUsername('');
        } catch (error) {
          console.error('Error inviting user:', error);
        }
        return;
      }
      
      alert(`Пользователь с именем "${username}" не найден. Доступные пользователи: ${allUsers.map(u => u.username).join(', ')}`);
      return;
    }
    
    try {
      await addTripMember(trip.id, { user_id: user.id, role: 'member' });
      await loadTripData(trip.id);
      setInviteUsername('');
    } catch (error) {
      console.error('Error inviting user:', error);
    }
  };

  const ensurePlace = async (osmPlace: OSMPlace) => {
    const placePayload = {
      name: osmPlace.display_name,
      lat: parseFloat(osmPlace.lat),
      lng: parseFloat(osmPlace.lon),
      osm_id: `${osmPlace.osm_type}:${osmPlace.osm_id}`,
      address: osmPlace.display_name,
    };
    return await createPlace(placePayload);
  };

  const handleSearchSuggestionPlaces = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!suggestionQuery.trim()) return;
    try {
      setIsSearchingSuggestions(true);
      const places = await searchPlaces(suggestionQuery.trim(), 10);
      setSuggestionSearchResults(places);
    } catch (error) {
      console.error('Error searching places:', error);
    } finally {
      setIsSearchingSuggestions(false);
    }
  };

  const handleAddSuggestion = async (osmPlace: OSMPlace) => {
    if (!trip) return;
    try {
      const place = await ensurePlace(osmPlace);
      await createSuggestion(trip.id, place.id, currentUserId);
      const updated = await getSuggestions(trip.id);
      setSuggestions(updated);
      setSuggestionSearchResults([]);
      setSuggestionQuery('');
    } catch (error) {
      console.error('Error creating suggestion:', error);
    }
  };

  const handleVote = async (suggestionId: number, vote: boolean) => {
    if (!trip) return;
    try {
      await voteOnSuggestion(suggestionId, currentUserId, vote);
      const updated = await getSuggestions(trip.id);
      setSuggestions(updated);
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleUpdateSuggestionStatus = async (suggestionId: number, status: 'accepted' | 'rejected') => {
    if (!trip) return;
    try {
      await updateSuggestionStatus(suggestionId, status);
      const updated = await getSuggestions(trip.id);
      setSuggestions(updated);
    } catch (error) {
      console.error('Error updating suggestion status:', error);
    }
  };

  const handleCreateExpense = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!trip) return;
    if (!trip.members || trip.members.length === 0) return;

    try {
      const memberIds = trip.members.map((m) => m.id);
      const baseShare = 1 / memberIds.length;
      const shares = memberIds.map((userId, idx) => {
        if (idx === memberIds.length - 1) {
          const prev = baseShare * (memberIds.length - 1);
          return { user_id: userId, share: 1 - prev };
        }
        return { user_id: userId, share: baseShare };
      });

      const payload = {
        trip_id: trip.id,
        title: newExpense.title,
        amount: parseFloat(newExpense.amount),
        currency: newExpense.currency,
        paid_by: parseInt(newExpense.paid_by, 10),
        date: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
        shares,
      };

      await createExpense(payload);
      const updated = await getTripExpenses(trip.id);
      setExpenses(updated);
      setNewExpense({ title: '', amount: '', paid_by: String(currentUserId), currency: 'RUB' });

      try {
        const b = await getTripBalances(trip.id);
        setBalances(b);
      } catch (error) {
        console.error('Error loading balances:', error);
      }
    } catch (error) {
      console.error('Error creating expense:', error);
    }
  };

  if (!trip) {
    return <div>Загрузка...</div>;
  }

  return (
    <div className="container-booking py-8">
      {/* Header */}
      <div className="booking-card p-6 mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          {trip.title}
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          {trip.description}
        </p>
        <div className="flex items-center space-x-6 text-sm text-gray-500">
          <div className="flex items-center">
            <CalendarIcon className="w-4 h-4 mr-1" />
            {trip.start_date} - {trip.end_date}
          </div>
          <div className="flex items-center">
            <UserGroupIcon className="w-4 h-4 mr-1" />
            {trip.members?.length || 0} участников
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-8 border-b border-gray-200 dark:border-gray-700">
        {[
          { id: 'info', label: 'Информация', icon: UserGroupIcon },
          { id: 'suggestions', label: `Предложения (${suggestions.length})`, icon: MapPinIcon },
          { id: 'routes', label: `Маршрут (${routes.length})`, icon: MapPinIcon },
          { id: 'expenses', label: `Расходы (${expenses.length})`, icon: CurrencyDollarIcon },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center space-x-2 px-4 py-3 border-b-2 font-medium text-sm transition-colors ${
              activeTab === tab.id
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'info' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Participants */}
            <div className="booking-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <UserGroupIcon className="w-5 h-5 mr-2" />
                Участники
              </h2>
              <div className="space-y-3">
                {trip.members?.map(member => (
                  <div key={member.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div>
                      <div className="font-medium text-gray-900 dark:text-white">
                        {member.username}
                      </div>
                      <div className="text-sm text-gray-500">{member.email}</div>
                    </div>
                    {trip.admin === member.id && (
                      <span className="px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                        Администратор
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Invite Users */}
            <div className="booking-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Пригласить пользователя
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Имя пользователя
                  </label>
                  <input
                    type="text"
                    value={inviteUsername}
                    onChange={(e) => setInviteUsername(e.target.value)}
                    placeholder="Например: ivanov"
                    className="booking-input"
                  />
                </div>
                <button
                  className="btn-primary w-full"
                  onClick={() => {
                    if (!inviteUsername.trim()) return;
                    handleInviteUser(inviteUsername.trim());
                  }}
                  disabled={!inviteUsername.trim()}
                >
                  Добавить в поездку
                </button>
              </div>

              <div className="mt-6">
                <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Все пользователи
                </h3>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {allUsers.map((u) => (
                    <div key={u.id} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
                      <span className="text-sm">
                        {u.username} ({u.email})
                      </span>
                      <button
                        className="btn-secondary text-sm px-3 py-1"
                        onClick={() => handleInviteUser(u.username)}
                        disabled={isMember(u.id)}
                      >
                        {isMember(u.id) ? 'Уже в поездке' : 'Пригласить'}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'suggestions' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Add Suggestion */}
            <div className="booking-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <PlusIcon className="w-5 h-5 mr-2" />
                Добавить предложение
              </h2>
              <form onSubmit={handleSearchSuggestionPlaces} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Поиск места
                  </label>
                  <div className="relative">
                    <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      value={suggestionQuery}
                      onChange={(e) => setSuggestionQuery(e.target.value)}
                      placeholder="Например: Эрмитаж"
                      className="booking-input pl-10"
                    />
                  </div>
                </div>
                <button 
                  type="submit" 
                  className="btn-primary w-full flex items-center justify-center"
                  disabled={isSearchingSuggestions}
                >
                  <MagnifyingGlassIcon className="w-5 h-5 mr-2" />
                  Найти
                </button>
              </form>

              {suggestionSearchResults.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Найденные места
                  </h3>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {suggestionSearchResults.map((p) => (
                      <div key={p.place_id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <span className="text-sm text-gray-900 dark:text-white line-clamp-2">
                          {p.display_name}
                        </span>
                        <button 
                          className="btn-secondary text-sm px-3 py-1" 
                          onClick={() => handleAddSuggestion(p)}
                        >
                          Предложить
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Suggestions List */}
            <div className="space-y-4">
              <div className="booking-card p-6">
                {/* Фильтры-табы */}
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Предложения ({suggestions.length})
                  </h2>
                  <div className="flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                    <button
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                        suggestionFilter === 'voting'
                          ? 'bg-white dark:bg-gray-600 text-primary-600 shadow-sm'
                          : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                      }`}
                      onClick={() => setSuggestionFilter('voting')}
                    >
                      <ChatBubbleLeftRightIcon className="w-4 h-4 inline mr-1" />
                      На рассмотрении
                    </button>
                    <button
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                        suggestionFilter === 'accepted'
                          ? 'bg-white dark:bg-gray-600 text-primary-600 shadow-sm'
                          : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                      }`}
                      onClick={() => setSuggestionFilter('accepted')}
                    >
                      <CheckIcon className="w-4 h-4 inline mr-1" />
                      Принятые
                    </button>
                    <button
                      className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                        suggestionFilter === 'rejected'
                          ? 'bg-white dark:bg-gray-600 text-primary-600 shadow-sm'
                          : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                      }`}
                      onClick={() => setSuggestionFilter('rejected')}
                    >
                      <XMarkIcon className="w-4 h-4 inline mr-1" />
                      Отклоненные
                    </button>
                  </div>
                </div>

                {/* Фильтрованные предложения */}
                {(() => {
                  const filteredSuggestions = suggestions.filter(s => 
                    suggestionFilter === 'voting' ? s.status === 'voting' : 
                    suggestionFilter === 'accepted' ? s.status === 'accepted' : 
                    s.status === 'rejected'
                  );
                  
                  return filteredSuggestions.length === 0 ? (
                    <div className="text-center py-8">
                      <MapPinIcon className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                      <p className="text-gray-500">
                        {suggestionFilter === 'voting' 
                          ? 'Предложений на рассмотрении нет' 
                          : suggestionFilter === 'accepted'
                          ? 'Принятых предложений нет'
                          : 'Отклоненных предложений нет'}
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {filteredSuggestions.map(suggestion => (
                        <div key={suggestion.id} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex-1">
                              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                                {suggestion.place.name}
                              </h3>
                              <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                                {suggestion.place.address}
                              </p>
                              <p className="text-xs text-gray-500">
                                Предложил: {suggestion.suggested_by_user.username}
                              </p>
                            </div>
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                              suggestion.status === 'accepted' 
                                ? 'bg-green-100 text-green-800'
                                : suggestion.status === 'rejected'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {suggestion.status === 'accepted' ? 'Принято' : 
                               suggestion.status === 'rejected' ? 'Отклонено' : 'Голосование'}
                            </span>
                          </div>

                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <span className="flex items-center">
                                <HandThumbUpIcon className="w-4 h-4 mr-1" />
                                {suggestion.votes_for}
                              </span>
                              <span className="flex items-center">
                                <HandThumbDownIcon className="w-4 h-4 mr-1" />
                                {suggestion.votes_against}
                              </span>
                            </div>

                            {suggestion.status === 'voting' && (
                              <div className="flex space-x-2">
                                <button 
                                  className="btn-secondary text-sm px-3 py-1" 
                                  onClick={() => handleVote(suggestion.id, true)}
                                >
                                  <HandThumbUpIcon className="w-4 h-4" />
                                </button>
                                <button
                                  className="btn-secondary text-sm px-3 py-1"
                                  onClick={() => handleVote(suggestion.id, false)}
                                >
                                  <HandThumbDownIcon className="w-4 h-4" />
                                </button>
                              </div>
                            )}

                            {trip.admin === currentUserId && suggestion.status === 'voting' && (
                              <div className="flex space-x-2">
                                <button
                                  className="btn-primary text-sm px-3 py-1"
                                  onClick={() => handleUpdateSuggestionStatus(suggestion.id, 'accepted')}
                                >
                                  <CheckCircleIcon className="w-4 h-4" />
                                </button>
                                <button
                                  className="btn-secondary text-sm px-3 py-1"
                                  onClick={() => handleUpdateSuggestionStatus(suggestion.id, 'rejected')}
                                >
                                  <XCircleIcon className="w-4 h-4" />
                                </button>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'routes' && (
          <RouteBuilder
            tripId={parseInt(id || '0')}
            routes={routes}
            suggestions={suggestions}
            onRouteAdded={(route) => setRoutes([...routes, route])}
          />
        )}

        {activeTab === 'expenses' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Add Expense */}
            <div className="booking-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <PlusIcon className="w-5 h-5 mr-2" />
                Добавить расход
              </h2>
              <form onSubmit={handleCreateExpense} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Название
                  </label>
                  <input
                    type="text"
                    value={newExpense.title}
                    onChange={(e) => setNewExpense({ ...newExpense, title: e.target.value })}
                    className="booking-input"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Сумма
                  </label>
                  <input
                    type="number"
                    value={newExpense.amount}
                    onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                    className="booking-input"
                    required
                    min={0}
                    step="0.01"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Валюта
                  </label>
                  <input
                    type="text"
                    value={newExpense.currency}
                    onChange={(e) => setNewExpense({ ...newExpense, currency: e.target.value })}
                    className="booking-input"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Оплатил
                  </label>
                  <select
                    value={newExpense.paid_by}
                    onChange={(e) => setNewExpense({ ...newExpense, paid_by: e.target.value })}
                    className="booking-input"
                  >
                    {trip.members?.map((m) => (
                      <option key={m.id} value={String(m.id)}>
                        {m.username}
                      </option>
                    ))}
                  </select>
                </div>

                <button type="submit" className="btn-primary w-full">
                  Добавить (разделить поровну)
                </button>
              </form>
            </div>

            {/* Expenses List */}
            <div className="space-y-6">
              {/* Balances */}
              {balances.length > 0 && (
                <div className="booking-card p-6">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                    <CurrencyDollarIcon className="w-5 h-5 mr-2" />
                    Долги
                  </h2>
                  <div className="space-y-3">
                    {balances.map((b: any, idx: number) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <span className="text-sm text-gray-900 dark:text-white">
                          {b.debtor_name} должен {b.creditor_name}
                        </span>
                        <span className="font-semibold text-primary-600">
                          {b.amount} ₽
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Expenses */}
              <div className="booking-card p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  Расходы ({expenses.length})
                </h2>
                {expenses.length === 0 ? (
                  <div className="text-center py-8">
                    <CurrencyDollarIcon className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-500">Расходов пока нет</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {expenses.map(expense => (
                      <div key={expense.id} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                              {expense.title}
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                              Оплатил: {expense.paid_by_user.username}
                            </p>
                            <p className="text-xs text-gray-500">
                              {new Date(expense.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="text-right">
                            <span className="text-lg font-bold text-primary-600">
                              {expense.amount} {expense.currency}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
