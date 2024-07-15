#Mathia Fiorelli 132139


#Funkcja do zaliczenia projektu
nash=function(game){
  #Tworzenie listy z rozmiarami gry
  dimensions_list <- list()
  for (i in seq_along(names(game))){
    dimension=dim(game[[i]])[i]
    name=names(game)[i]
    dimensions_list[[name]]=1:dimension
  }
  str=expand.grid(dimensions_list)
  values=c()
  vnames=c()
  cnames=c()
  #Dodanie pomocniczych kolumn
  for (i in seq_along(names(game))){
    value=game[[i]][as.matrix(str)]
    values=cbind(values,value)
    vnames=c(vnames,paste('value',i,sep=''))
    cnames=c(cnames,paste('change',i,sep=''))
    
  }
  str=cbind(str,values)
  colnames(str)[(ncol(str) - length(vnames) + 1):ncol(str)] <- vnames
  for (i in 1:dim(str)[1]){
    #print('############')
    #print(paste('Row:',i))
    for (j in seq_along(names(game))){
      player=names(game)[j]
      current_value=str[[player]][i]
      #print(paste('Current Player:',player,'Current strategy:',str[[player]][i],'Current value:',current_value))
      #Pozostali gracze
      other_players = names(game)[names(game) != player]
      #print(paste('Other Players:',other_players))
      # Strategie pozostałych graczy w tym wierszu
      other_players_str=str[[other_players]][i]
      #print(paste('Other Players Strategies:',other_players_str))
      # Wypłaty obecnego gracza z pominięciem obecnego wiersza dla niezmiennych strategii pozostałych graczy
      player_values=str[str[other_players]==other_players_str,]
      player_values$Row_Index = as.integer(rownames(player_values))
      player_values=player_values[player_values$Row_Index!=i,]
      player_values=player_values[[vnames[j]]]
      #print(paste('Current Player other values:',player_values))
      player_values_bool=player_values>current_value
      #cat('Bool list:', as.character(player_values_bool), '\n')
      str[[cnames[j]]][i]=any(player_values_bool)
      #print('*********')
    }
    nash_value=(!any(unlist(str[i,cnames])))
    str$Nash[i]=nash_value
  }
  return_obj=str[str$Nash,names(game)]
  return(return_obj)

}


game_prison <- list(
  "player1" = array(c(5, 10, 1, 2), dim = c(2, 2)),
  "player2" = array(c(5, 1, 10, 2), dim = c(2, 2))
)

game_stag <- list(
  "player1" = array(c(3, 2, 0, 2), dim = c(2, 2)),
  "player2" = array(c(3, 0, 2, 2), dim = c(2, 2))
)



