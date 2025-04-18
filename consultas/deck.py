db.battles.aggregate([
  {
    $addFields: {
      battleTimeDate: {
        $dateFromString: {
          dateString: "$battleTime",
          format: "%Y%m%dT%H%M%S.%LZ"
        }
      }
    }
  },
  {
    $match: {
      battleTimeDate: {
        $gte: ISODate("2025-01-01T00:00:00Z"),
        $lte: ISODate("2025-12-31T23:59:59Z")
      }
    }
  },
  {
    $addFields: {
      vitoria: {
        $gt: [
          { $arrayElemAt: ["$team.crowns", 0] },
          { $max: "$opponent.crowns" }
        ]
      }
    }
  },
  {
    $group: {
      _id: "$team.cards",
      totalPartidas: { $sum: 1 },
      totalVitorias: {
        $sum: {
          $cond: ["$vitoria", 1, 0]
        }
      }
    }
  },
  {
    $addFields: {
      taxaVitorias: {
        $multiply: [
          { $divide: ["$totalVitorias", "$totalPartidas"] },
          100
        ]
      }
    }
  },
  {
    $match: {
      taxaVitorias: { $gte: 60 } // aqui é a porcentagem mínima
    }
  },
  {
    $project: {
      _id: 0,
      deck: "$_id",
      totalPartidas: 1,
      totalVitorias: 1,
      taxaVitorias: { $round: ["$taxaVitorias", 2] }
    }
  },
  {
    $sort: { taxaVitorias: -1 }
  }
]);
