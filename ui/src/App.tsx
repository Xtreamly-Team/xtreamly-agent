import {Outlet, Route, Routes} from "react-router-dom";
import NoMatch from "./pages/NoMatch";
import Header from "./components/header/Header";
import {Container} from "@mantine/core";
import Agent from "./pages/Agent";


function Layout() {
  return (
      <div className="layout">
        <Header/>
        <Container pt={100} size="xl">
          <Outlet/>
        </Container>
      </div>
  );
}

function App() {
  return (
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout/>}>
              <Route index element={<Agent/>}/>
              <Route path="*" element={<NoMatch/>}/>
          </Route>
        </Routes>
      </div>
  );
}

export default App;
