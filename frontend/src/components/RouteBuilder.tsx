import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import { Icon } from 'leaflet';
import { Route, Suggestion, OSMPlace } from '../types';
import { searchPlaces, createPlace, createRoute } from '../services/api';
import { MagnifyingGlassIcon, PlusIcon, MapPinIcon, CalendarIcon, CurrencyDollarIcon, MapIcon } from '@heroicons/react/24/outline';
import 'leaflet/dist/leaflet.css';

interface RouteBuilderProps {
  tripId: number;
  routes: Route[];
  suggestions: Suggestion[];
  onRouteAdded: (route: Route) => void;
}

export const RouteBuilder: React.FC<RouteBuilderProps> = (props) => {
  const { tripId, routes, suggestions, onRouteAdded } = props;
  const [selectedPlace, setSelectedPlace] = useState<OSMPlace | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<OSMPlace[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [highlightedRouteId, setHighlightedRouteId] = useState<number | null>(null);
  const [showRoutePath, setShowRoutePath] = useState(false);
  const [newRoute, setNewRoute] = useState({
    day_number: '1',
    order_in_day: '1',
    planned_time: '',
    estimated_cost: '',
    notes: '',
  });

  // Создаем кастомные иконки с номерами
  const createNumberedIcon = (number: number) => {
    return new Icon({
      iconUrl: `data:image/svg+xml;base64,${btoa(`
        <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
          <circle cx="20" cy="20" r="18" fill="#3b82f6" stroke="#fff" stroke-width="2"/>
          <text x="20" y="28" text-anchor="middle" fill="white" font-size="16" font-weight="bold">${number}</text>
        </svg>
      `)}`,
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -40],
      className: 'numbered-marker'
    });
  };

  // Стандартная иконка для выбранного места
  const standardIcon = new Icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  // Выделенная иконка для подсвеченной метки
  const highlightedIcon = new Icon({
    iconUrl: `data:image/svg+xml;base64,${btoa(`
      <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="20" r="18" fill="#ef4444" stroke="#fff" stroke-width="3"/>
        <text x="20" y="28" text-anchor="middle" fill="white" font-size="16" font-weight="bold">!</text>
      </svg>
    `)}`,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40],
    className: 'highlighted-marker'
  });

  // Получаем все одобренные места и разделяем их на добавленные и недобавленные
  const allApprovedPlaces = suggestions
    .filter(s => s.status === 'accepted')
    .map(s => s.place);
    
  const approvedPlaces = allApprovedPlaces.filter(place => 
    !routes.some(route => {
      // Сравниваем по имени (обрезая пробелы и приводя к нижнему регистру)
      const placeName = place.name?.trim().toLowerCase() || '';
      const routeName = route.place.name?.trim().toLowerCase() || '';
      return placeName === routeName;
    })
  );
  const alreadyAddedPlaces = allApprovedPlaces.filter(place => 
    routes.some(route => {
      const placeName = place.name?.trim().toLowerCase() || '';
      const routeName = route.place.name?.trim().toLowerCase() || '';
      return placeName === routeName;
    })
  );

  // Автоматически обновляем порядковый номер при изменении количества маршрутов
  useEffect(() => {
    if (!selectedPlace) {
      setNewRoute(prev => ({
        ...prev,
        order_in_day: String(routes.length + 1)
      }));
    }
  }, [routes.length, selectedPlace]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const results = await searchPlaces(searchQuery, 10);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching places:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddToMap = async (place: OSMPlace) => {
    setIsAdding(true);
    try {
      // Сначала создаем место в базе данных
      const createdPlace = await createPlace({
        name: place.display_name,
        lat: parseFloat(place.lat),
        lng: parseFloat(place.lon),
        osm_id: place.osm_id ? place.osm_id.toString() : null,
        address: place.display_name,
      });

      // Убедимся, что order_in_day - это валидное число
      const orderInDay = parseInt(newRoute.order_in_day) || 1;
      
      // Затем создаем маршрут
      const routePayload = {
        trip_id: tripId,
        place_id: createdPlace.id,
        day_number: parseInt(newRoute.day_number) || 1,
        order_in_day: orderInDay,
        planned_time: newRoute.planned_time || undefined,
        estimated_cost: newRoute.estimated_cost ? parseFloat(newRoute.estimated_cost) : undefined,
        notes: newRoute.notes || undefined,
        added_by: 1, // TODO: использовать текущего пользователя
      };
      
      const route = await createRoute(routePayload);

      onRouteAdded(route);
      // Очищаем форму и выбранное место после успешного добавления
      setSelectedPlace(null);
      setSearchQuery('');
      setSearchResults([]);
      // Порядковый номер обновится автоматически через useEffect
    } catch (error: any) {
      console.error('Error adding route:', error);
      console.error('Error details:', error.response?.data);
    } finally {
      setIsAdding(false);
    }
  };

  const handleSelectExistingPlace = (place: OSMPlace) => {
    setSelectedPlace(place);
    setSearchQuery('');
    setSearchResults([]);
    // Если это новый выбор (не смена уже выбранного места), устанавливаем следующий порядковый номер
    if (!selectedPlace || selectedPlace.place_id !== place.place_id) {
      setNewRoute(prev => ({
        ...prev,
        order_in_day: String(routes.length + 1)
      }));
    }
  };

  // Получаем координаты для центра карты
  const getCenterCoords = () => {
    if (routes.length > 0) {
      const avgLat = routes.reduce((sum, r) => sum + r.place.lat, 0) / routes.length;
      const avgLng = routes.reduce((sum, r) => sum + r.place.lng, 0) / routes.length;
      return [avgLat, avgLng] as [number, number];
    }
    return [55.7558, 37.6173] as [number, number]; // Москва по умолчанию
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Левая панель - добавление места */}
      <div className="lg:col-span-1">
        <div className="booking-card p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <PlusIcon className="w-5 h-5 mr-2" />
            Добавить место на маршрут
          </h2>
          
          {/* Выпадающий список с предложенными местами */}
          {allApprovedPlaces.length > 0 && (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Предложенные места
              </label>
              <select 
                className="booking-input"
                onChange={(e) => {
                  const place = approvedPlaces.find(p => p.id.toString() === e.target.value);
                  if (place) {
                    const osmPlace: OSMPlace = {
                      place_id: place.id,
                      licence: '',
                      osm_type: '',
                      osm_id: place.osm_id ? parseInt(place.osm_id) : 0,
                      lat: place.lat.toString(),
                      lon: place.lng.toString(),
                      display_name: place.name,
                      address: {},
                      boundingbox: []
                    };
                    handleSelectExistingPlace(osmPlace);
                  }
                }}
                value=""
              >
                <option value="">Выберите из предложенных...</option>
                {approvedPlaces.map(place => (
                  <option key={place.id} value={place.id}>
                    {place.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Поиск новых мест */}
          <form onSubmit={handleSearch} className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Найти новое место
            </label>
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                className="booking-input pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Например: Эрмитаж"
              />
            </div>
            <button 
              type="submit" 
              className="btn-primary w-full mt-3 flex items-center justify-center"
              disabled={isSearching || !searchQuery.trim()}
            >
              <MagnifyingGlassIcon className="w-5 h-5 mr-2" />
              {isSearching ? 'Поиск...' : 'Найти'}
            </button>
          </form>

          {/* Результаты поиска */}
          {searchResults.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Результаты поиска
              </h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {searchResults.map(place => (
                  <div 
                    key={place.place_id} 
                    className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    onClick={() => handleSelectExistingPlace(place)}
                  >
                    <div className="text-sm font-medium text-gray-900 dark:text-white line-clamp-2">
                      {place.display_name}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Детали выбранного места и форма добавления */}
          {selectedPlace && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Выбранное место
              </h3>
              <div className="p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg mb-4">
                <div className="text-sm font-medium text-primary-900 dark:text-primary-100 line-clamp-2">
                  {selectedPlace.display_name}
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      День
                    </label>
                    <input
                      type="number"
                      className="booking-input"
                      value={newRoute.day_number}
                      onChange={(e) => setNewRoute({ ...newRoute, day_number: e.target.value })}
                      min="1"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Порядок
                    </label>
                    <input
                      type="number"
                      className="booking-input"
                      value={newRoute.order_in_day}
                      onChange={(e) => setNewRoute({ ...newRoute, order_in_day: e.target.value })}
                      min="1"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <CalendarIcon className="w-4 h-4 inline mr-1" />
                    Время (HH:MM)
                  </label>
                  <input
                    type="text"
                    className="booking-input"
                    value={newRoute.planned_time}
                    onChange={(e) => setNewRoute({ ...newRoute, planned_time: e.target.value })}
                    placeholder="12:30"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <CurrencyDollarIcon className="w-4 h-4 inline mr-1" />
                    Примерная стоимость
                  </label>
                  <input
                    type="number"
                    className="booking-input"
                    value={newRoute.estimated_cost}
                    onChange={(e) => setNewRoute({ ...newRoute, estimated_cost: e.target.value })}
                    min="0"
                    step="0.01"
                    placeholder="0.00"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Заметки
                  </label>
                  <textarea
                    className="booking-input"
                    value={newRoute.notes}
                    onChange={(e) => setNewRoute({ ...newRoute, notes: e.target.value })}
                    rows={2}
                  />
                </div>

                <button 
                  className="btn-primary w-full flex items-center justify-center"
                  onClick={() => handleAddToMap(selectedPlace)}
                  disabled={isAdding}
                >
                  <MapPinIcon className="w-5 h-5 mr-2" />
                  {isAdding ? 'Добавление...' : 'Добавить на карту'}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Список меток на карте */}
        {routes.length > 0 && (
          <div className="booking-card p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <MapPinIcon className="w-5 h-5 mr-2" />
              Метки на карте ({routes.length})
            </h2>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {routes
                .sort((a, b) => a.day_number - b.day_number || a.order_in_day - b.order_in_day)
                .map((route, index) => (
                <div 
                  key={route.id} 
                  className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
                    highlightedRouteId === route.id 
                      ? 'bg-primary-100 dark:bg-primary-900/30 border border-primary-300' 
                      : 'bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600'
                  }`}
                  onClick={() => setHighlightedRouteId(highlightedRouteId === route.id ? null : route.id)}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {route.place.name}
                      </div>
                      <div className="text-xs text-gray-500">
                        День {route.day_number}, Пункт {route.order_in_day}
                        {route.planned_time && ` • ${route.planned_time}`}
                        {route.estimated_cost && ` • ${route.estimated_cost} ₽`}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Кнопка соединения маршрута */}
            {routes.length > 1 && (
              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  className={`w-full flex items-center justify-center px-4 py-2 rounded-lg font-medium transition-colors ${
                    showRoutePath
                      ? 'bg-primary-600 text-white hover:bg-primary-700'
                      : 'btn-secondary'
                  }`}
                  onClick={() => setShowRoutePath(!showRoutePath)}
                >
                  <MapIcon className="w-5 h-5 mr-2" />
                  {showRoutePath ? 'Скрыть маршрут' : 'Соединить в маршрут'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Правая панель - карта */}
      <div className="lg:col-span-2">
        <div className="booking-card p-0 h-full">
          <div className="h-96 lg:h-full min-h-[500px] rounded-booking-lg overflow-hidden">
            <MapContainer 
              center={getCenterCoords()} 
              zoom={10} 
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {/* Маркеры существующих маршрутов */}
              {routes
                .sort((a, b) => a.day_number - b.day_number || a.order_in_day - b.order_in_day)
                .map((route, index) => (
                <Marker 
                  key={route.id} 
                  position={[route.place.lat, route.place.lng]}
                  icon={highlightedRouteId === route.id ? highlightedIcon : createNumberedIcon(index + 1)}
                >
                  <Popup>
                    <div className="text-sm">
                      <h4 className="font-semibold">{route.place.name}</h4>
                      <p><strong>День {route.day_number}, Пункт {route.order_in_day}</strong></p>
                      {route.planned_time && <p>Время: {route.planned_time}</p>}
                      {route.estimated_cost && <p>Стоимость: {route.estimated_cost} ₽</p>}
                      {route.notes && <p>Заметки: {route.notes}</p>}
                    </div>
                  </Popup>
                </Marker>
              ))}

              {/* Линия маршрута */}
              {showRoutePath && routes.length > 1 && (
                <Polyline
                  positions={routes
                    .sort((a, b) => a.day_number - b.day_number || a.order_in_day - b.order_in_day)
                    .map(route => [route.place.lat, route.place.lng])}
                  color="#3b82f6"
                  weight={3}
                  opacity={0.8}
                  dashArray="10, 5"
                />
              )}

              {/* Маркер выбранного места */}
              {selectedPlace && (
                <Marker 
                  position={[parseFloat(selectedPlace.lat), parseFloat(selectedPlace.lon)]}
                  icon={standardIcon}
                >
                  <Popup>
                    <div className="text-sm">
                      <h4 className="font-semibold">{selectedPlace.display_name}</h4>
                      <p>Это место будет добавлено в маршрут</p>
                    </div>
                  </Popup>
                </Marker>
              )}
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
