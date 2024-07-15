#MAthia Fiorelli 132139

#Funkcja obliczająca całkę
integrate3d2 = function(fun, xlim, ylim, n)
{
  #Podział po x i y
  x_range = seq(min(xlim),max(xlim),length.out=n)
  y_range = seq(min(ylim),max(ylim),length.out=n)
  #Pole powierzchni
  area = (max(xlim)-min(xlim))*(max(ylim)-min(ylim))
  #Macierz z wartościami funkcji
  fun_matrix <- outer(y_range, x_range, FUN = funkcja)
  #Objętość
  volume = area*sum(fun_matrix)/n^2
  return (volume)
}

#Dane wejściowe do zadeklarowania:
#Funkcja
funkcja= function(x, y){cos(x*y)}
##PRzedział x i y
xlim = c(0, 1)
ylim = c(0, 1)
#Liczba podziałów
n = 10000
integral = integrate3d2(funkcja, xlim, ylim, n)
integral

### Example 2 (low n)
integrate3d(
  f = function(x, y) {cos(x) * y},
  over = list(x = c(0, pi / 2), y = c(0, 1)),
  n = 10^2)
