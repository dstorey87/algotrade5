import { Middleware } from 'redux';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';

const middleware: Middleware[] = [thunk];
export const mockStore = configureStore(middleware);

export const createMockStore = (initialState = {}) => {
  const store = mockStore(initialState);
  // Mock dispatch but preserve the original implementation
  const originalDispatch = store.dispatch;
  store.dispatch = jest.fn((action) => originalDispatch(action)) as any;
  return store;
};