# db.battles.aggregate([
#   {
#     $addFields: {
#       battleTimeDate: {
#         $dateFromString: {
#           dateString: "$battleTime",
#           format: "%Y%m%dT%H%M%S.%LZ"
#         }
#       }
#     }
#   },
#   {
#     $match: {
#       "team.cards.name": {$all:["Musketeer","Skeletons","Giant"]}  
#       battleTimeDate: {
#         $gte: ISODate("2025-01-01T00:00:00Z"),
#         $lte: ISODate("2025-12-31T23:59:59Z")
#       }
#     }
#   },
#   {
#     $addFields: {
#       derrotas: {
#         $lt: [
#           { $arrayElemAt: ["$team.crowns", 0] },
#           { $max: "$opponent.crowns" }
#         ]
#       }
#     }
#   },
#    $group: {
#       _id: { deck: "$team.cards" },
#       totalDerrotas: {
#         $sum: {
#           $cond: ["$derrota", 1, 0]
#         }
#       },
#       totalPartidas: { $sum: 1 }
#     }
#   },
#   {
#     $project: {
#       _id: 0,
#       deck: "$_id.deck",
#       totalPartidas: 1,
#       totalDerrotas: 1,
#       taxaDerrotas: {
#         $multiply: [
#           { $divide: ["$totalDerrotas", "$totalPartidas"] },
#           100
#         ]
#       }
#     }
#   },
#   {
#     $sort: { taxaDerrotas: -1 }
#   }
# ])

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
      "team.0.cards.name": { $all: ["Musketeer", "Skeletons", "Miner"] },
      battleTimeDate: {
        $gte: ISODate("2025-04-01T00:00:00.000Z"),
        $lte: ISODate("2025-04-17T23:59:59.999Z")
      }
    }
  },
  {
    $addFields: {
      derrota: {
        $lt: [
          { $arrayElemAt: ["$team.crowns", 0] },
          { $arrayElemAt: ["$opponent.crowns", 0] }
        ]
      }
    }
  },
  {
    $group: {
      _id: null,
      totalDerrotas: {
        $sum: {
          $cond: ["$derrota", 1, 0]
        }
      },
      totalPartidas: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      totalPartidas: 1,
      totalDerrotas: 1,
      taxaDerrotas: {
        $round: [
          {
            $multiply: [
              { $divide: ["$totalDerrotas", "$totalPartidas"] },
              100
            ]
          },
          2
        ]
      }
    }
  }
])



 