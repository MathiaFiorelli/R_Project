#Mathia Fiorelli 132139


#Funkcja służąca do zalewania. Zwraca zalaną macierz
flood = function(result)
{
  #Współrzędne reszty labirynru i ścian
  indices_t <- which(result, arr.ind = TRUE)
  indices_f <- which(result==FALSE, arr.ind = TRUE)
  
  #x - kolumny, y- wiersze
  x1 <- indices_t[,2]
  x2 <- indices_f[,2]
  y1 <- indices_t[,1]
  y2 <- indices_f[,1]
  
  # labirynt znajduje się między wartościami minimalnymi i maksymalnymi wierszy i kolumn 
  x_min <- min(x2)
  x_max <- max(x2)
  y_min <- min(y2)
  y_max <- max(y2)
  
  # Zamiana wartości z logicznych na liczbowe: 
  # 0 - ściana, 1 - niezalany punkt, 2 - zalany punkt, 3 - zalany w poprzednich iteracjach
  numeric_data <- result
  numeric_data[indices_t]=1
  numeric_data[indices_f]=0
  #Zapoczątkowanie ziarna od któego zalewanie się rozpocznie
  numeric_data[x_min, y_min] <- 2
  
  # Kierunki poruszania się po sąsiadach
  dir_v <- c(1, -1, 0, 0)
  dir_h <- c(0, 0, 1, -1)
  
  #Wymiary macierzy
  matrix_dimensions <- dim(numeric_data)
  
  num_rows <- matrix_dimensions[1]
  num_cols <- matrix_dimensions[2]
  
  # Zalanie tych miejsc które są zdala od labiryntu
  numeric_data[,1:x_min]=2
  numeric_data[,x_max:num_cols]=2
  numeric_data[1:y_min,]=2
  numeric_data[y_max:num_rows,]=2
  
  #Algorytm zalewania
  while (TRUE) {
    #data_old to macierz do której się porównuje zmienianą macierz. 
    #Jeżeli po jednej iteracji nie ma zmian, to algorytm kończy pracę
    data_old <- numeric_data
    #Współrzędne punktów które zostały dopiero co zalane
    coordinates <- which(numeric_data == 2, arr.ind = TRUE)
    #Zmiana wartości na "wcześniej zalane"
    numeric_data[numeric_data == 2] <- 3
    rows <- coordinates[, 1]
    cols <- coordinates[, 2]
    
    # Zalewanie sąsiadów którzy nie są ścaną labiryntu
    for (i in seq_along(rows)) {
      for (d in seq_along(dir_v)) {
        row_new <- rows[i] + dir_v[d]
        col_new <- cols[i] + dir_h[d]
        if ((y_min - 1 <= row_new) && (row_new <= y_max + 1) &&
            (x_min - 1 <= col_new) && (col_new <= x_max + 1)) {
          n_val <- numeric_data[row_new, col_new]
          if (n_val == 1) {
            numeric_data[row_new, col_new] <- 2
          }
        }
      }
    }
    
    if (all(data_old == numeric_data)) {
      break
    }
  }
  
  return(numeric_data)
}

# Funkcja sprawdzająca czy istnieje połączenie między zadanym punktem startowym a docelowym.
# Sprawdza czy zarówno punkt docelowy jak i startowy zostały zalane.
pathQ = function(result,destination,start)
{
  start_x=start$x
  start_y=start$y
  d_x=destination$x
  d_y=destination$y
  
  
  flooded=flood(result)
  
  solution=FALSE
  for (x in d_x)
  {
    for (y in d_y)
      if (flooded[y,x]>1)
      {
        solution=TRUE
        break
      }
    if (solution)
    {
      break
    }
  }
  
  val_start=flooded[start_y,start_x]
  check = (val_start>1)&solution
  return(check)
  
}

result <- readRDS("C:\\Users\\mathi\\OneDrive\\Documents\\Studia\\SGH\\R\\P1\\maze.RDS")

### End region
logoPosition <- list(y = 387:413, x = 322:348)

### Starting point
startPoint <- list(x = 1, y = 1)

x=pathQ(result,logoPosition,startPoint)
print(x)

### End region
endPosition <- list(x = 220:230, y = 325:335)

### Starting point
startPoint <- list(x = 1, y = 1)
x=pathQ(result,logoPosition,startPoint)
print(x)