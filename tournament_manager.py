from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json


class GameResult(Enum):
    WHITE_WIN = 1
    BLACK_WIN = 0
    DRAW = 0.5
    NO_RESULT = None


@dataclass
class Player:
    """Represents a chess player in the tournament."""
    player_id: str
    name: str
    rating: int

    def __hash__(self):
        return hash(self.player_id)

    def __eq__(self, other):
        return isinstance(other, Player) and self.player_id == other.player_id


@dataclass
class Game:
    """Represents a single game/match in the tournament."""
    game_id: str
    round_number: int
    white_player: Player
    black_player: Player
    result: Optional[GameResult] = None
    date_played: Optional[datetime] = None
    notes: str = ""

    def get_white_score(self) -> float:
        """Returns the score for white player."""
        if self.result is None:
            return 0.0
        return float(self.result.value) if self.result.value is not None else 0.0

    def get_black_score(self) -> float:
        """Returns the score for black player."""
        if self.result is None:
            return 0.0
        if self.result == GameResult.WHITE_WIN:
            return 0.0
        elif self.result == GameResult.BLACK_WIN:
            return 1.0
        elif self.result == GameResult.DRAW:
            return 0.5
        return 0.0


@dataclass
class PlayerStats:
    """Statistics for a player in the tournament."""
    player: Player
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    total_score: float = 0.0
    rounds_missed: int = 0
    buchholz_score: float = 0.0  # Sum of opponents' scores
    whites_played: int = 0       # Number of times player had white pieces

    def get_win_percentage(self) -> float:
        """Calculate win percentage."""
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100

    def get_average_rating(self) -> float:
        """Get average opponent rating."""
        if self.games_played == 0:
            return 0.0
        return self.player.rating


@dataclass
class Round:
    """Represents a round in the tournament."""
    round_number: int
    games: Dict[str, Game] = field(default_factory=dict)
    scheduled_date: Optional[datetime] = None

    def add_game(self, game: Game):
        """Add a game to the round."""
        self.games[game.game_id] = game

    def get_games_for_player(self, player: Player) -> List[Game]:
        """Get all games for a specific player in this round."""
        return [g for g in self.games.values()
                if g.white_player == player or g.black_player == player]


class SwissTournament:
    """Manages a Swiss system chess tournament."""

    def __init__(self, tournament_id: str, name: str, club_name: str):
        self.tournament_id = tournament_id
        self.name = name
        self.club_name = club_name
        self.created_date = datetime.now()
        self.players: Dict[str, Player] = {}
        self.rounds: Dict[int, Round] = {}
        self.current_round: int = 0
        self.player_stats: Dict[str, PlayerStats] = {}
        self.pairings_locked: bool = False

    def add_player(self, player_id: str, name: str, rating: int) -> Player:
        """Add a player to the tournament."""
        if player_id in self.players:
            raise ValueError(f"Player {player_id} already exists")

        player = Player(player_id=player_id, name=name, rating=rating)
        self.players[player_id] = player
        self.player_stats[player_id] = PlayerStats(player=player)
        return player

    def remove_player(self, player_id: str):
        """Remove a player from the tournament."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} not found")
        del self.players[player_id]
        if player_id in self.player_stats:
            del self.player_stats[player_id]

    def start_round(self, round_number: int, scheduled_date: Optional[datetime] = None) -> Round:
        """Start a new round."""
        if round_number in self.rounds:
            raise ValueError(f"Round {round_number} already exists")

        self.current_round = round_number
        round_obj = Round(round_number=round_number, scheduled_date=scheduled_date)
        self.rounds[round_number] = round_obj
        return round_obj

    def generate_pairings(self, round_number: int, byes: List[str] = None) -> List[Tuple[Player, Player]]:
        """
        Generate Swiss pairings for a round.
        Players in 'byes' list will receive a bye (missed round, 0 pts).
        An odd player left over receives an auto-bye worth 1 point.
        Returns list of (white_player, black_player) tuples.
        """
        if byes is None:
            byes = []

        # Build set of already-played matchups to avoid rematches
        played_pairs: set = set()
        for rnd in self.rounds.values():
            for game in rnd.games.values():
                a = game.white_player.player_id
                b = game.black_player.player_id
                played_pairs.add((a, b))
                played_pairs.add((b, a))

        # Sort available players by score desc, then rating desc (Swiss order)
        available_players = [p for pid, p in self.players.items() if pid not in byes]
        available_players.sort(
            key=lambda p: (-self.player_stats[p.player_id].total_score, -p.rating)
        )

        pairings = []
        paired = set()

        for i, player in enumerate(available_players):
            if player.player_id in paired:
                continue

            opponent = None
            # Prefer nearest unpaired player we haven't played before
            for j in range(i + 1, len(available_players)):
                candidate = available_players[j]
                if candidate.player_id in paired:
                    continue
                if (player.player_id, candidate.player_id) not in played_pairs:
                    opponent = candidate
                    break

            # Fallback: allow rematch if no unplayed opponent is available
            if opponent is None:
                for j in range(i + 1, len(available_players)):
                    candidate = available_players[j]
                    if candidate.player_id not in paired:
                        opponent = candidate
                        break

            if opponent is None:
                continue  # will be caught as auto-bye below

            # Assign colors to balance each player's white/black history
            p_whites = self.player_stats[player.player_id].whites_played
            o_whites = self.player_stats[opponent.player_id].whites_played
            if p_whites <= o_whites:
                white, black = player, opponent
            else:
                white, black = opponent, player

            pairings.append((white, black))
            paired.add(player.player_id)
            paired.add(opponent.player_id)

        # Auto-bye: odd player left without a pairing earns 1 point
        if len(available_players) % 2 == 1:
            unpaired = [p for p in available_players if p.player_id not in paired]
            if unpaired:
                auto_bye_pid = unpaired[0].player_id
                self.record_bye(auto_bye_pid, round_number, score=1.0)

        return pairings

    def create_games(self, round_number: int, pairings: List[Tuple[Player, Player]]):
        """Create games from pairings."""
        if round_number not in self.rounds:
            raise ValueError(f"Round {round_number} not found")

        round_obj = self.rounds[round_number]

        for idx, (white, black) in enumerate(pairings):
            game_id = f"{self.tournament_id}_R{round_number}_G{idx}"
            game = Game(
                game_id=game_id,
                round_number=round_number,
                white_player=white,
                black_player=black
            )
            round_obj.add_game(game)

    def record_result(self, game_id: str, result: GameResult, notes: str = ""):
        """Record the result of a game."""
        # Find the game
        game = None
        for round_obj in self.rounds.values():
            if game_id in round_obj.games:
                game = round_obj.games[game_id]
                break

        if game is None:
            raise ValueError(f"Game {game_id} not found")

        # Record result
        game.result = result
        game.date_played = datetime.now()
        game.notes = notes

        # Update player stats
        white_stats = self.player_stats[game.white_player.player_id]
        black_stats = self.player_stats[game.black_player.player_id]

        white_stats.games_played += 1
        black_stats.games_played += 1
        white_stats.whites_played += 1

        white_score = game.get_white_score()
        black_score = game.get_black_score()

        white_stats.total_score += white_score
        black_stats.total_score += black_score

        if result == GameResult.WHITE_WIN:
            white_stats.wins += 1
            black_stats.losses += 1
        elif result == GameResult.BLACK_WIN:
            black_stats.wins += 1
            white_stats.losses += 1
        elif result == GameResult.DRAW:
            white_stats.draws += 1
            black_stats.draws += 1

    def record_bye(self, player_id: str, round_number: int, score: float = 0.0):
        """Record that a player missed a round (bye).

        score=1.0 for system-assigned byes (odd player out, earns a full point).
        score=0.0 for manually selected byes (absent/voluntary, no point awarded).
        """
        if player_id not in self.player_stats:
            raise ValueError(f"Player {player_id} not found")

        stats = self.player_stats[player_id]
        stats.rounds_missed += 1
        stats.total_score += score

    def get_standings(self) -> List[PlayerStats]:
        """Get tournament standings sorted by score."""
        self.calculate_buchholz_scores()
        standings = list(self.player_stats.values())
        standings.sort(
            key=lambda s: (-s.total_score, -s.buchholz_score, -s.player.rating)
        )
        return standings

    def get_round_games(self, round_number: int) -> List[Game]:
        """Get all games in a specific round."""
        if round_number not in self.rounds:
            raise ValueError(f"Round {round_number} not found")
        return list(self.rounds[round_number].games.values())

    def get_player_games(self, player_id: str) -> List[Game]:
        """Get all games played by a player."""
        if player_id not in self.players:
            raise ValueError(f"Player {player_id} not found")

        player = self.players[player_id]
        games = []
        for round_obj in self.rounds.values():
            games.extend(round_obj.get_games_for_player(player))
        return games

    def calculate_buchholz_scores(self):
        """Calculate buchholz scores (sum of opponents' scores)."""
        for player_id, stats in self.player_stats.items():
            player = self.players[player_id]
            buchholz = 0.0

            for game in self.get_player_games(player_id):
                if game.result is not None:
                    opponent = game.black_player if game.white_player == player else game.white_player
                    opponent_stats = self.player_stats[opponent.player_id]
                    buchholz += opponent_stats.total_score

            stats.buchholz_score = buchholz

    def get_tournament_info(self) -> Dict:
        """Get tournament information."""
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "club_name": self.club_name,
            "created_date": self.created_date.isoformat(),
            "current_round": self.current_round,
            "total_players": len(self.players),
            "total_rounds": len(self.rounds)
        }


# Example usage
# if __name__ == "__main__":
#     # Create a tournament
#     tournament = SwissTournament("CLUB2024", "Club Championship 2024", "Local Chess Club")

#     # Add players
#     players = [
#         ("p1", "Alice Johnson", 1600),
#         ("p2", "Bob Smith", 1550),
#         ("p3", "Charlie Brown", 1500),
#         ("p4", "Diana Lee", 1620),
#         ("p5", "Eve Martinez", 1480),
#     ]

#     for player_id, name, rating in players:
#         tournament.add_player(player_id, name, rating)

#     # Start round 1
#     round_1 = tournament.start_round(1, datetime.now())
#     pairings = tournament.generate_pairings(1)
#     tournament.create_games(1, pairings)

#     # Record some results
#     games = tournament.get_round_games(1)
#     if len(games) > 0:
#         tournament.record_result(games[0].game_id, GameResult.WHITE_WIN)
#     if len(games) > 1:
#         tournament.record_result(games[1].game_id, GameResult.DRAW)

#     # Show standings
#     print("\n=== Tournament Standings ===")
#     standings = tournament.get_standings()
#     for rank, stats in enumerate(standings, 1):
#         print(f"{rank}. {stats.player.name}: {stats.total_score} pts ({stats.games_played} games)")

#     print("\n=== Tournament Info ===")
#     info = tournament.get_tournament_info()
#     for key, value in info.items():
#         print(f"{key}: {value}")
