import { useState, useEffect } from 'react';

interface Processor {
  id: number;
  product: string;
  status: string;
  release_date: string;
  code_name: string;
  cores: number;
  threads: number;
  lithography: number;
  max_turbo_freq: number;
  base_freq: number;
  tdp: number;
}

interface Filters {
  year: string;
  status: string;
  codeName: string;
  cores: string;
  threads: string;
  lithography: string;
}

export default function ProcessorList() {
  const [processors, setProcessors] = useState<Processor[]>([]);
  const [filteredProcessors, setFilteredProcessors] = useState<Processor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({
    year: '',
    status: '',
    codeName: '',
    cores: '',
    threads: '',
    lithography: '',
  });

  useEffect(() => {
    fetch('/api/processors')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setProcessors(data);
        setFilteredProcessors(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching processors:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    let result = [...processors];

    if (filters.year) {
      result = result.filter(p => p.release_date.includes(filters.year));
    }
    if (filters.status) {
      result = result.filter(p => p.status === filters.status);
    }
    if (filters.codeName) {
      result = result.filter(p => p.code_name === filters.codeName);
    }
    if (filters.cores) {
      result = result.filter(p => p.cores === parseInt(filters.cores));
    }
    if (filters.threads) {
      result = result.filter(p => p.threads === parseInt(filters.threads));
    }
    if (filters.lithography) {
      result = result.filter(p => p.lithography === parseFloat(filters.lithography));
    }

    setFilteredProcessors(result);
  }, [filters, processors]);

  const getUniqueValues = (field: keyof Processor) => {
    return Array.from(new Set(processors.map(p => p[field])))
      .filter(value => value !== null && value !== undefined)
      .sort();
  };

  const getUniqueYears = () => {
    return Array.from(new Set(processors.map(p => p.release_date.slice(-4))))
      .filter(year => year)
      .sort();
  };

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>;
  }

  if (error) {
    return <div className="bg-red-50 border-l-4 border-red-500 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm text-red-700">Error: {error}</p>
        </div>
      </div>
    </div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 bg-white p-4 rounded-lg shadow">
        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.year}
          onChange={(e) => setFilters(prev => ({ ...prev, year: e.target.value }))}
        >
          <option value="">All Years</option>
          {getUniqueYears().map(year => (
            <option key={year} value={year}>{year}</option>
          ))}
        </select>

        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.status}
          onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
        >
          <option value="">All Status</option>
          {getUniqueValues('status').map(status => (
            <option key={status} value={status}>{status}</option>
          ))}
        </select>

        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.codeName}
          onChange={(e) => setFilters(prev => ({ ...prev, codeName: e.target.value }))}
        >
          <option value="">All Code Names</option>
          {getUniqueValues('code_name').map(name => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>

        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.cores}
          onChange={(e) => setFilters(prev => ({ ...prev, cores: e.target.value }))}
        >
          <option value="">All Cores</option>
          {getUniqueValues('cores').map(cores => (
            <option key={cores} value={cores}>{cores}</option>
          ))}
        </select>

        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.threads}
          onChange={(e) => setFilters(prev => ({ ...prev, threads: e.target.value }))}
        >
          <option value="">All Threads</option>
          {getUniqueValues('threads').map(threads => (
            <option key={threads} value={threads}>{threads}</option>
          ))}
        </select>

        <select
          className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200"
          value={filters.lithography}
          onChange={(e) => setFilters(prev => ({ ...prev, lithography: e.target.value }))}
        >
          <option value="">All Lithography</option>
          {getUniqueValues('lithography').map(litho => (
            <option key={litho} value={litho}>{litho}nm</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Release Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Code Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cores</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Threads</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lithography</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max Turbo Freq</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Base Freq</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">TDP</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredProcessors.map((processor) => (
              <tr key={processor.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{processor.product}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    processor.status === 'Launched' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {processor.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.release_date}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.code_name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.cores}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.threads}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.lithography}nm</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.max_turbo_freq}GHz</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.base_freq}GHz</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{processor.tdp}W</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
